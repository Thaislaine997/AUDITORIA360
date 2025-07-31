import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  Alert,
  IconButton,
  Drawer,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip,
  LinearProgress,
} from '@mui/material';
import {
  ArrowBack,
  PlayArrow,
  Pause,
  Speed,
  Warning,
  CheckCircle,
  Error,
  Timeline,
  Settings,
} from '@mui/icons-material';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Text, Line } from '@react-three/drei';
import * as THREE from 'three';

interface Employee {
  id: string;
  name: string;
  status: 'active' | 'vacation' | 'leave' | 'terminated';
  hasIssues: boolean;
}

interface PayrollEvent {
  id: string;
  name: string;
  type: 'calculation' | 'send' | 'validation' | 'report';
  progress: number;
  status: 'pending' | 'processing' | 'completed' | 'error';
  affectedEmployees: string[];
  errorCount: number;
}

interface LoomKnot {
  id: string;
  employeeId: string;
  eventId: string;
  position: [number, number, number];
  severity: 'warning' | 'error' | 'critical';
  description: string;
}

interface ComplianceLoomProps {
  onBack: () => void;
}

// Animated Loom Thread (Employee)
const LoomThread: React.FC<{ 
  employee: Employee; 
  position: [number, number, number];
  onThreadClick: (employee: Employee) => void;
}> = ({ employee, position, onThreadClick }) => {
  const threadRef = useRef<THREE.Mesh>(null);
  
  const getThreadColor = () => {
    switch (employee.status) {
      case 'active': return '#4CAF50';
      case 'vacation': return '#FFEB3B';
      case 'leave': return '#9E9E9E';
      case 'terminated': return '#F44336';
      default: return '#2196F3';
    }
  };

  const getEmissiveIntensity = () => {
    return employee.hasIssues ? 0.5 : 0.1;
  };

  useFrame((state) => {
    if (threadRef.current && employee.hasIssues) {
      const time = state.clock.getElapsedTime();
      threadRef.current.material.emissiveIntensity = 0.3 + Math.sin(time * 3) * 0.2;
    }
  });

  return (
    <group position={position}>
      <mesh 
        ref={threadRef}
        onClick={() => onThreadClick(employee)}
        position={[0, 0, 0]}
      >
        <cylinderGeometry args={[0.05, 0.05, 8, 8]} />
        <meshPhongMaterial 
          color={getThreadColor()}
          emissive={employee.hasIssues ? '#ff0000' : '#000000'}
          emissiveIntensity={getEmissiveIntensity()}
        />
      </mesh>
      
      <Text
        position={[0, -4.5, 0]}
        fontSize={0.2}
        color="white"
        anchorX="center"
        anchorY="middle"
        rotation={[0, 0, -Math.PI / 2]}
      >
        {employee.name.split(' ')[0]}
      </Text>
    </group>
  );
};

// Animated Shuttle (Payroll Event)
const PayrollShuttle: React.FC<{ 
  event: PayrollEvent; 
  position: [number, number, number];
  onShuttleClick: (event: PayrollEvent) => void;
}> = ({ event, position, onShuttleClick }) => {
  const shuttleRef = useRef<THREE.Mesh>(null);
  
  const getShuttleColor = () => {
    switch (event.status) {
      case 'completed': return '#4CAF50';
      case 'processing': return '#FF9800';
      case 'error': return '#F44336';
      default: return '#2196F3';
    }
  };

  useFrame((state) => {
    if (shuttleRef.current && event.status === 'processing') {
      const time = state.clock.getElapsedTime();
      shuttleRef.current.position.x = position[0] + Math.sin(time * 2) * 2;
    }
  });

  return (
    <group position={position}>
      <mesh 
        ref={shuttleRef}
        onClick={() => onShuttleClick(event)}
        position={[0, 0, 0]}
      >
        <boxGeometry args={[1, 0.3, 0.3]} />
        <meshPhongMaterial 
          color={getShuttleColor()}
          emissive={event.status === 'error' ? '#ff0000' : '#000000'}
          emissiveIntensity={event.status === 'error' ? 0.3 : 0.1}
        />
      </mesh>
      
      <Text
        position={[0, 0.5, 0]}
        fontSize={0.15}
        color="white"
        anchorX="center"
        anchorY="middle"
      >
        {event.name}
      </Text>
      
      {/* Progress indicator */}
      <mesh position={[0, -0.7, 0]}>
        <boxGeometry args={[event.progress / 100 * 2, 0.1, 0.1]} />
        <meshPhongMaterial color="#4CAF50" />
      </mesh>
    </group>
  );
};

// Loom Knot (Error/Issue)
const LoomKnot: React.FC<{ 
  knot: LoomKnot; 
  onKnotClick: (knot: LoomKnot) => void;
}> = ({ knot, onKnotClick }) => {
  const knotRef = useRef<THREE.Mesh>(null);

  const getKnotColor = () => {
    switch (knot.severity) {
      case 'warning': return '#FF9800';
      case 'error': return '#F44336';
      case 'critical': return '#8B0000';
      default: return '#FF9800';
    }
  };

  useFrame((state) => {
    if (knotRef.current) {
      const time = state.clock.getElapsedTime();
      knotRef.current.scale.setScalar(0.8 + Math.sin(time * 4) * 0.3);
      knotRef.current.rotation.y += 0.02;
    }
  });

  return (
    <mesh 
      ref={knotRef}
      position={knot.position}
      onClick={() => onKnotClick(knot)}
    >
      <octahedronGeometry args={[0.3, 0]} />
      <meshPhongMaterial 
        color={getKnotColor()}
        emissive={getKnotColor()}
        emissiveIntensity={0.5}
      />
    </mesh>
  );
};

// eSocial Wave Effect
const ESocialWave: React.FC<{ 
  isActive: boolean; 
  progress: number; 
  employees: Employee[];
}> = ({ isActive, progress, employees }) => {
  const waveRef = useRef<THREE.Mesh>(null);

  useFrame((state) => {
    if (waveRef.current && isActive) {
      const time = state.clock.getElapsedTime();
      waveRef.current.position.x = -6 + (progress / 100) * 12;
      waveRef.current.material.opacity = 0.3 + Math.sin(time * 3) * 0.2;
    }
  });

  if (!isActive) return null;

  return (
    <mesh ref={waveRef} position={[-6, 0, 0]}>
      <sphereGeometry args={[0.5, 16, 16]} />
      <meshPhongMaterial 
        color="#00BCD4"
        transparent
        opacity={0.5}
        emissive="#00BCD4"
        emissiveIntensity={0.3}
      />
    </mesh>
  );
};

const ComplianceLoom: React.FC<ComplianceLoomProps> = ({ onBack }) => {
  const [isRunning, setIsRunning] = useState(false);
  const [selectedEmployee, setSelectedEmployee] = useState<Employee | null>(null);
  const [selectedEvent, setSelectedEvent] = useState<PayrollEvent | null>(null);
  const [selectedKnot, setSelectedKnot] = useState<LoomKnot | null>(null);
  const [eSocialProgress, setESocialProgress] = useState(0);
  const [isESocialActive, setIsESocialActive] = useState(false);
  const [detailsPanelOpen, setDetailsPanelOpen] = useState(false);

  // Mock data
  const employees: Employee[] = [
    { id: '1', name: 'João Silva', status: 'active', hasIssues: false },
    { id: '2', name: 'Maria Santos', status: 'active', hasIssues: true },
    { id: '3', name: 'Pedro Costa', status: 'vacation', hasIssues: false },
    { id: '4', name: 'Ana Oliveira', status: 'active', hasIssues: true },
    { id: '5', name: 'Carlos Lima', status: 'leave', hasIssues: false },
    { id: '6', name: 'Julia Ferreira', status: 'active', hasIssues: false },
  ];

  const payrollEvents: PayrollEvent[] = [
    {
      id: '1',
      name: 'Cálculo Férias',
      type: 'calculation',
      progress: 75,
      status: 'processing',
      affectedEmployees: ['1', '2', '3'],
      errorCount: 1,
    },
    {
      id: '2',
      name: 'Fechamento Ponto',
      type: 'calculation',
      progress: 100,
      status: 'completed',
      affectedEmployees: ['1', '2', '3', '4', '5', '6'],
      errorCount: 0,
    },
    {
      id: '3',
      name: 'Cálculo 13º',
      type: 'calculation',
      progress: 45,
      status: 'processing',
      affectedEmployees: ['1', '4', '6'],
      errorCount: 2,
    },
    {
      id: '4',
      name: 'Envio eSocial',
      type: 'send',
      progress: 0,
      status: 'pending',
      affectedEmployees: ['1', '2', '3', '4', '5', '6'],
      errorCount: 0,
    },
  ];

  const loomKnots: LoomKnot[] = [
    {
      id: '1',
      employeeId: '2',
      eventId: '1',
      position: [-2, 2, 0],
      severity: 'warning',
      description: 'Funcionário afastado recebendo cálculo de férias',
    },
    {
      id: '2',
      employeeId: '4',
      eventId: '3',
      position: [2, -1, 0],
      severity: 'error',
      description: 'Dados de admissão incompletos para cálculo do 13º',
    },
  ];

  // eSocial simulation
  const handleESocialLaunch = () => {
    setIsESocialActive(true);
    setESocialProgress(0);
    
    const interval = setInterval(() => {
      setESocialProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsESocialActive(false);
          return 100;
        }
        return prev + 2;
      });
    }, 100);
  };

  const handleThreadClick = (employee: Employee) => {
    setSelectedEmployee(employee);
    setDetailsPanelOpen(true);
  };

  const handleShuttleClick = (event: PayrollEvent) => {
    setSelectedEvent(event);
    setDetailsPanelOpen(true);
  };

  const handleKnotClick = (knot: LoomKnot) => {
    setSelectedKnot(knot);
    setDetailsPanelOpen(true);
  };

  const getOverallHealth = () => {
    const totalKnots = loomKnots.length;
    const criticalKnots = loomKnots.filter(k => k.severity === 'critical').length;
    const errorKnots = loomKnots.filter(k => k.severity === 'error').length;
    
    if (criticalKnots > 0) return { color: 'error', text: 'Crítico' };
    if (errorKnots > 0) return { color: 'warning', text: 'Atenção' };
    if (totalKnots > 0) return { color: 'info', text: 'Monitoramento' };
    return { color: 'success', text: 'Saudável' };
  };

  const overallHealth = getOverallHealth();

  return (
    <Box sx={{ height: '100vh', width: '100vw', position: 'relative', bgcolor: '#1a1a1a' }}>
      {/* Header */}
      <Box
        sx={{
          position: 'absolute',
          top: 16,
          left: 16,
          right: 16,
          zIndex: 10,
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <Button
          startIcon={<ArrowBack />}
          onClick={onBack}
          sx={{ color: 'white', bgcolor: 'rgba(255,255,255,0.1)' }}
        >
          Voltar ao Bioma
        </Button>
        
        <Typography variant="h4" sx={{ color: 'white', fontWeight: 'bold' }}>
          🧵 Tear da Conformidade
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            startIcon={isRunning ? <Pause /> : <PlayArrow />}
            onClick={() => setIsRunning(!isRunning)}
            sx={{ color: 'white', bgcolor: 'rgba(76, 175, 80, 0.8)' }}
          >
            {isRunning ? 'Pausar' : 'Iniciar'} Tear
          </Button>
          
          <Button
            startIcon={<Speed />}
            onClick={handleESocialLaunch}
            disabled={isESocialActive}
            sx={{ color: 'white', bgcolor: 'rgba(0, 188, 212, 0.8)' }}
          >
            Lançar eSocial
          </Button>
        </Box>
      </Box>

      {/* Status Panel */}
      <Alert
        severity={overallHealth.color as any}
        sx={{
          position: 'absolute',
          top: 80,
          left: 16,
          zIndex: 10,
          bgcolor: 'rgba(255,255,255,0.9)',
        }}
      >
        <strong>Status do Tear: {overallHealth.text}</strong> - {loomKnots.length} nós detectados
      </Alert>

      {/* eSocial Progress */}
      {isESocialActive && (
        <Paper
          sx={{
            position: 'absolute',
            top: 80,
            right: 16,
            zIndex: 10,
            p: 2,
            bgcolor: 'rgba(255,255,255,0.9)',
            minWidth: 200,
          }}
        >
          <Typography variant="subtitle2" gutterBottom>
            Onda eSocial
          </Typography>
          <LinearProgress 
            variant="determinate" 
            value={eSocialProgress} 
            sx={{ mb: 1 }}
          />
          <Typography variant="body2" color="text.secondary">
            {eSocialProgress.toFixed(0)}% concluído
          </Typography>
        </Paper>
      )}

      {/* 3D Canvas */}
      <Canvas
        camera={{ position: [0, 0, 15], fov: 60 }}
        style={{ width: '100%', height: '100%' }}
      >
        <ambientLight intensity={0.4} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        <pointLight position={[-10, -10, -10]} intensity={0.5} />
        
        {/* Employee Threads (Vertical) */}
        {employees.map((employee, index) => {
          const x = (index - employees.length / 2) * 2;
          return (
            <LoomThread
              key={employee.id}
              employee={employee}
              position={[x, 0, 0]}
              onThreadClick={handleThreadClick}
            />
          );
        })}
        
        {/* Payroll Event Shuttles (Horizontal) */}
        {payrollEvents.map((event, index) => {
          const y = (index - payrollEvents.length / 2) * 2;
          return (
            <PayrollShuttle
              key={event.id}
              event={event}
              position={[0, y, 1]}
              onShuttleClick={handleShuttleClick}
            />
          );
        })}
        
        {/* Loom Knots (Errors) */}
        {loomKnots.map((knot) => (
          <LoomKnot
            key={knot.id}
            knot={knot}
            onKnotClick={handleKnotClick}
          />
        ))}
        
        {/* eSocial Wave */}
        <ESocialWave
          isActive={isESocialActive}
          progress={eSocialProgress}
          employees={employees}
        />
        
        <OrbitControls enablePan={true} enableZoom={true} enableRotate={true} />
      </Canvas>

      {/* Details Panel */}
      <Drawer
        anchor="right"
        open={detailsPanelOpen}
        onClose={() => setDetailsPanelOpen(false)}
      >
        <Box sx={{ width: 400, p: 3 }}>
          {selectedEmployee && (
            <>
              <Typography variant="h6" gutterBottom>
                👤 Fio: {selectedEmployee.name}
              </Typography>
              <Chip 
                label={selectedEmployee.status}
                color={selectedEmployee.hasIssues ? 'error' : 'success'}
                sx={{ mb: 2 }}
              />
              <Typography variant="body2" color="text.secondary">
                Status: {selectedEmployee.status}
                {selectedEmployee.hasIssues && ' - Possui inconsistências'}
              </Typography>
            </>
          )}
          
          {selectedEvent && (
            <>
              <Typography variant="h6" gutterBottom>
                🚀 Lançadeira: {selectedEvent.name}
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={selectedEvent.progress} 
                sx={{ mb: 2 }}
              />
              <Typography variant="body2" color="text.secondary" gutterBottom>
                Progresso: {selectedEvent.progress}%
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Funcionários afetados: {selectedEvent.affectedEmployees.length}
              </Typography>
              {selectedEvent.errorCount > 0 && (
                <Typography variant="body2" color="error">
                  Erros detectados: {selectedEvent.errorCount}
                </Typography>
              )}
            </>
          )}
          
          {selectedKnot && (
            <>
              <Typography variant="h6" gutterBottom color="error">
                ⚠️ Nó Detectado
              </Typography>
              <Chip 
                label={selectedKnot.severity}
                color={selectedKnot.severity === 'critical' ? 'error' : 'warning'}
                sx={{ mb: 2 }}
              />
              <Typography variant="body2" color="text.secondary">
                {selectedKnot.description}
              </Typography>
              <Button
                variant="contained"
                color="primary"
                fullWidth
                sx={{ mt: 2 }}
                onClick={() => {
                  // Handle knot resolution
                  setDetailsPanelOpen(false);
                }}
              >
                Resolver Nó
              </Button>
            </>
          )}
        </Box>
      </Drawer>
    </Box>
  );
};

export default ComplianceLoom;