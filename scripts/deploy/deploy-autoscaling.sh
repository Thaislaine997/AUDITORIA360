#!/bin/bash

# AUDITORIA360 Auto-scaling Deployment Script
# Phase 3: Performance Optimization Infrastructure

set -euo pipefail

# Configuration
CLUSTER_NAME="auditoria360-cluster"
NAMESPACE="auditoria360"
REDIS_PASSWORD=$(openssl rand -base64 32)
DB_PASSWORD=${DATABASE_PASSWORD:-""}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check if kubectl is installed
    if ! command -v kubectl &> /dev/null; then
        error "kubectl is not installed. Please install kubectl first."
    fi
    
    # Check if helm is installed (optional)
    if ! command -v helm &> /dev/null; then
        warn "Helm is not installed. Some optional features may not be available."
    fi
    
    # Check cluster connectivity
    if ! kubectl cluster-info &> /dev/null; then
        error "Cannot connect to Kubernetes cluster. Please check your kubeconfig."
    fi
    
    log "Prerequisites check completed successfully"
}

# Create namespace
create_namespace() {
    log "Creating namespace: ${NAMESPACE}"
    
    kubectl create namespace ${NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -
    
    # Label namespace for monitoring
    kubectl label namespace ${NAMESPACE} monitoring=enabled --overwrite
    
    log "Namespace ${NAMESPACE} created/updated"
}

# Create secrets
create_secrets() {
    log "Creating application secrets..."
    
    # Check if required environment variables are set
    if [[ -z "${DATABASE_URL:-}" ]]; then
        error "DATABASE_URL environment variable is required"
    fi
    
    if [[ -z "${R2_ACCESS_KEY_ID:-}" ]]; then
        error "R2_ACCESS_KEY_ID environment variable is required"
    fi
    
    if [[ -z "${R2_SECRET_ACCESS_KEY:-}" ]]; then
        error "R2_SECRET_ACCESS_KEY environment variable is required"
    fi
    
    # Create main application secrets
    kubectl create secret generic auditoria360-secrets \
        --from-literal=database-url="${DATABASE_URL}" \
        --from-literal=redis-url="redis://redis-service:6379" \
        --from-literal=r2-access-key="${R2_ACCESS_KEY_ID}" \
        --from-literal=r2-secret-key="${R2_SECRET_ACCESS_KEY}" \
        --from-literal=secret-key="${SECRET_KEY:-$(openssl rand -base64 32)}" \
        --namespace=${NAMESPACE} \
        --dry-run=client -o yaml | kubectl apply -f -
    
    # Create Redis password secret
    kubectl create secret generic redis-secret \
        --from-literal=password="${REDIS_PASSWORD}" \
        --namespace=${NAMESPACE} \
        --dry-run=client -o yaml | kubectl apply -f -
    
    log "Secrets created successfully"
}

# Deploy Redis cache
deploy_redis() {
    log "Deploying Redis cache cluster..."
    
    kubectl apply -f deploy/kubernetes/redis-deployment.yaml -n ${NAMESPACE}
    
    # Wait for Redis to be ready
    log "Waiting for Redis to be ready..."
    kubectl wait --for=condition=available --timeout=300s deployment/redis-cache -n ${NAMESPACE}
    
    log "Redis cache deployed successfully"
}

# Deploy main application
deploy_application() {
    log "Deploying AUDITORIA360 API application..."
    
    # Apply configuration
    kubectl apply -f deploy/kubernetes/api-deployment.yaml -n ${NAMESPACE}
    
    # Wait for application to be ready
    log "Waiting for application to be ready..."
    kubectl wait --for=condition=available --timeout=600s deployment/auditoria360-api -n ${NAMESPACE}
    
    # Check if HPA is working
    kubectl get hpa auditoria360-api-hpa -n ${NAMESPACE}
    
    log "Application deployed successfully"
}

# Setup monitoring
setup_monitoring() {
    log "Setting up performance monitoring..."
    
    # Create monitoring resources (if Prometheus is available)
    cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ServiceMonitor
metadata:
  name: auditoria360-metrics
  namespace: ${NAMESPACE}
  labels:
    app: auditoria360-api
spec:
  selector:
    matchLabels:
      app: auditoria360-api
  endpoints:
  - port: http
    path: /metrics
    interval: 30s
---
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: auditoria360-alerts
  namespace: ${NAMESPACE}
  labels:
    app: auditoria360-api
spec:
  groups:
  - name: auditoria360.rules
    rules:
    - alert: HighResponseTime
      expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High response time detected"
        description: "95th percentile response time is above 1 second"
    
    - alert: HighErrorRate
      expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
      for: 2m
      labels:
        severity: critical
      annotations:
        summary: "High error rate detected"
        description: "Error rate is above 10%"
    
    - alert: CacheHitRateLow
      expr: redis_keyspace_hits_total / (redis_keyspace_hits_total + redis_keyspace_misses_total) < 0.8
      for: 10m
      labels:
        severity: warning
      annotations:
        summary: "Cache hit rate is low"
        description: "Redis cache hit rate is below 80%"
EOF
    
    log "Monitoring setup completed"
}

# Verify deployment
verify_deployment() {
    log "Verifying deployment..."
    
    # Check all pods are running
    kubectl get pods -n ${NAMESPACE}
    
    # Check services
    kubectl get services -n ${NAMESPACE}
    
    # Check HPA status
    kubectl get hpa -n ${NAMESPACE}
    
    # Test API health endpoint
    log "Testing API health endpoint..."
    
    # Port forward to test locally
    kubectl port-forward -n ${NAMESPACE} service/auditoria360-api-service 8080:80 &
    PORT_FORWARD_PID=$!
    
    sleep 5
    
    # Test health endpoint
    if curl -f http://localhost:8080/health > /dev/null 2>&1; then
        log "✅ Health check passed"
    else
        warn "❌ Health check failed"
    fi
    
    # Test performance endpoint
    if curl -f http://localhost:8080/api/v1/performance/health > /dev/null 2>&1; then
        log "✅ Performance monitoring endpoint accessible"
    else
        warn "❌ Performance monitoring endpoint not accessible"
    fi
    
    # Kill port forward
    kill $PORT_FORWARD_PID 2>/dev/null || true
    
    log "Deployment verification completed"
}

# Load testing
run_load_test() {
    log "Running basic load test..."
    
    # Use kubectl run to create a temporary pod for load testing
    kubectl run load-test \
        --image=busybox \
        --restart=Never \
        --rm -i \
        --namespace=${NAMESPACE} \
        -- sh -c "
            echo 'Running load test...'
            for i in \$(seq 1 100); do
                wget -q -O- http://auditoria360-api-service/health &
            done
            wait
            echo 'Load test completed'
        " || warn "Load test failed"
    
    # Check if HPA scaled up
    sleep 30
    kubectl get hpa auditoria360-api-hpa -n ${NAMESPACE}
    
    log "Load test completed"
}

# Performance optimization verification
verify_performance_optimization() {
    log "Verifying performance optimizations..."
    
    # Check Redis is working
    redis_pod=$(kubectl get pods -n ${NAMESPACE} -l app=redis-cache -o jsonpath='{.items[0].metadata.name}')
    if [[ -n "$redis_pod" ]]; then
        redis_info=$(kubectl exec -n ${NAMESPACE} $redis_pod -- redis-cli info keyspace)
        log "Redis info: $redis_info"
    fi
    
    # Check application metrics
    api_pod=$(kubectl get pods -n ${NAMESPACE} -l app=auditoria360-api -o jsonpath='{.items[0].metadata.name}')
    if [[ -n "$api_pod" ]]; then
        log "Checking application performance metrics..."
        kubectl logs -n ${NAMESPACE} $api_pod --tail=50 | grep -i "performance\|cache\|optimization" || true
    fi
    
    log "Performance optimization verification completed"
}

# Cleanup function
cleanup() {
    log "Cleaning up temporary resources..."
    # Kill any background processes
    jobs -p | xargs -r kill 2>/dev/null || true
}

# Main deployment function
main() {
    log "Starting AUDITORIA360 auto-scaling deployment..."
    
    # Set trap for cleanup
    trap cleanup EXIT
    
    # Run deployment steps
    check_prerequisites
    create_namespace
    create_secrets
    deploy_redis
    deploy_application
    setup_monitoring
    verify_deployment
    run_load_test
    verify_performance_optimization
    
    log "🎉 AUDITORIA360 auto-scaling deployment completed successfully!"
    log ""
    log "Next steps:"
    log "1. Configure DNS to point to the load balancer"
    log "2. Set up SSL/TLS certificates"
    log "3. Configure monitoring dashboards"
    log "4. Run comprehensive performance tests"
    log ""
    log "To access the application:"
    log "kubectl port-forward -n ${NAMESPACE} service/auditoria360-api-service 8080:80"
    log "Then visit: http://localhost:8080"
}

# Script options
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "cleanup")
        log "Cleaning up deployment..."
        kubectl delete namespace ${NAMESPACE} --ignore-not-found=true
        log "Cleanup completed"
        ;;
    "status")
        log "Checking deployment status..."
        kubectl get all -n ${NAMESPACE}
        kubectl get hpa -n ${NAMESPACE}
        ;;
    "logs")
        log "Showing application logs..."
        kubectl logs -n ${NAMESPACE} -l app=auditoria360-api --tail=100 -f
        ;;
    "test")
        log "Running performance test..."
        run_load_test
        verify_performance_optimization
        ;;
    *)
        echo "Usage: $0 {deploy|cleanup|status|logs|test}"
        echo ""
        echo "Commands:"
        echo "  deploy  - Deploy the complete auto-scaling infrastructure"
        echo "  cleanup - Remove all deployed resources"
        echo "  status  - Check deployment status"
        echo "  logs    - Show application logs"
        echo "  test    - Run performance tests"
        exit 1
        ;;
esac