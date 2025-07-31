import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Typography,
  Paper,
  Fab,
  Tooltip,
  Zoom,
  Alert,
  Button,
  IconButton,
} from '@mui/material';
import {
  ArrowBack,
  Favorite,
  Psychology,
  WaterDrop,
  Forest,
  Timeline,
} from '@mui/icons-material';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Text } from '@react-three/drei';
import * as THREE from 'three';

interface ClientRiver {
  id: string;
  name: string;
  employeeCount: number;
  healthStatus: 'healthy' | 'warning' | 'critical';
  flowSpeed: number;
  compliance: number;
}

interface Employee {
  id: string;
  name: string;
  status: 'active' | 'vacation' | 'leave' | 'terminated';
  notifications: number;
}

interface KairosOrganicDashboardProps {
  onBackToTraditional: () => void;
}

// Pulsing Heart Component
const PulsingHeart: React.FC<{ pulse: number; onClick: () => void }> = ({ pulse, onClick }) => {
  const heartRef = useRef<THREE.Mesh>(null);

  useEffect(() => {
    if (heartRef.current) {
      const scale = 1 + Math.sin(pulse * 0.1) * 0.2;
      heartRef.current.scale.setScalar(scale);
    }
  }, [pulse]);

  return (
    <mesh ref={heartRef} position={[0, 0, 0]} onClick={onClick}>
      <sphereGeometry args={[2, 32, 32]} />
      <meshPhongMaterial 
        color={new THREE.Color().setHSL((Math.sin(pulse * 0.05) + 1) * 0.15, 0.8, 0.6)}
        emissive={new THREE.Color().setHSL(0, 0.5, 0.1)}
      />
      <Text
        position={[0, 0, 2.5]}
        fontSize={0.5}
        color="white"
        anchorX="center"
        anchorY="middle"
      >
        Coração DP
      </Text>
    </mesh>
  );
};

// Client River Component
const ClientRiver: React.FC<{ 
  river: ClientRiver; 
  index: number; 
  onRiverClick: (river: ClientRiver) => void;
}> = ({ river, index, onRiverClick }) => {
  const riverRef = useRef<THREE.Mesh>(null);
  const angle = (index / 8) * Math.PI * 2;
  const distance = 6;
  
  const getColor = () => {
    switch (river.healthStatus) {
      case 'healthy': return '#4CAF50';
      case 'warning': return '#FF9800';
      case 'critical': return '#F44336';
      default: return '#2196F3';
    }
  };

  const getOpacity = () => {
    return Math.max(0.3, river.compliance / 100);
  };

  return (
    <group position={[
      Math.cos(angle) * distance,
      Math.sin(index * 0.5) * 2,
      Math.sin(angle) * distance
    ]}>
      <mesh 
        ref={riverRef}
        onClick={() => onRiverClick(river)}
      >
        <cylinderGeometry args={[river.employeeCount / 50, river.employeeCount / 100, 4, 8]} />
        <meshPhongMaterial 
          color={getColor()}
          opacity={getOpacity()}
          transparent
        />
      </mesh>
      <Text
        position={[0, 3, 0]}
        fontSize={0.3}
        color="white"
        anchorX="center"
        anchorY="middle"
      >
        {river.name}
      </Text>
      <Text
        position={[0, 2.5, 0]}
        fontSize={0.2}
        color="lightblue"
        anchorX="center"
        anchorY="middle"
      >
        {river.employeeCount} colaboradores
      </Text>
    </group>
  );
};

// Employee Tree Component for Forest View
const EmployeeTree: React.FC<{ 
  employee: Employee; 
  position: [number, number, number];
}> = ({ employee, position }) => {
  const getTreeColor = () => {
    switch (employee.status) {
      case 'active': return '#4CAF50';
      case 'vacation': return '#FFEB3B';
      case 'leave': return '#9E9E9E';
      case 'terminated': return '#795548';
      default: return '#4CAF50';
    }
  };

  const getTreeHeight = () => {
    return employee.status === 'terminated' ? 0.5 : 2;
  };

  return (
    <group position={position}>
      {/* Tree trunk */}
      <mesh position={[0, 0, 0]}>
        <cylinderGeometry args={[0.1, 0.15, getTreeHeight(), 8]} />
        <meshPhongMaterial color="#8D6E63" />
      </mesh>
      
      {/* Tree foliage */}
      {employee.status !== 'terminated' && (
        <mesh position={[0, getTreeHeight() * 0.7, 0]}>
          <sphereGeometry args={[0.8, 16, 16]} />
          <meshPhongMaterial color={getTreeColor()} />
        </mesh>
      )}
      
      {/* Notification birds */}
      {employee.notifications > 0 && Array.from({ length: Math.min(employee.notifications, 3) }).map((_, i) => (
        <mesh 
          key={i}
          position={[
            Math.cos(i * 2.1) * 1.5,
            getTreeHeight() + 1 + Math.sin(Date.now() * 0.003 + i) * 0.3,
            Math.sin(i * 2.1) * 1.5
          ]}
        >
          <sphereGeometry args={[0.1, 8, 8]} />
          <meshPhongMaterial color="#FFD700" />
        </mesh>
      ))}
      
      {/* Employee name */}
      <Text
        position={[0, -0.5, 0]}
        fontSize={0.2}
        color="white"
        anchorX="center"
        anchorY="middle"
      >
        {employee.name.split(' ')[0]}
      </Text>
    </group>
  );
};

const KairosOrganicDashboard: React.FC<KairosOrganicDashboardProps> = ({ onBackToTraditional }) => {
  const [pulse, setPulse] = useState(0);
  const [viewMode, setViewMode] = useState<'biome' | 'forest'>('biome');
  const [selectedRiver, setSelectedRiver] = useState<ClientRiver | null>(null);

  // Mock data for demonstration
  const clientRivers: ClientRiver[] = [
    { id: '1', name: 'Empresa Alpha', employeeCount: 150, healthStatus: 'healthy', flowSpeed: 1.2, compliance: 95 },
    { id: '2', name: 'Beta Corp', employeeCount: 80, healthStatus: 'warning', flowSpeed: 0.8, compliance: 75 },
    { id: '3', name: 'Gamma Ltd', employeeCount: 200, healthStatus: 'critical', flowSpeed: 0.3, compliance: 45 },
    { id: '4', name: 'Delta Inc', employeeCount: 120, healthStatus: 'healthy', flowSpeed: 1.1, compliance: 88 },
    { id: '5', name: 'Epsilon SA', employeeCount: 90, healthStatus: 'warning', flowSpeed: 0.7, compliance: 65 },
    { id: '6', name: 'Zeta Group', employeeCount: 180, healthStatus: 'healthy', flowSpeed: 1.3, compliance: 92 },
    { id: '7', name: 'Eta Systems', employeeCount: 60, healthStatus: 'critical', flowSpeed: 0.4, compliance: 40 },
    { id: '8', name: 'Theta Co', employeeCount: 110, healthStatus: 'healthy', flowSpeed: 1.0, compliance: 85 },
  ];

  const mockEmployees: Employee[] = [
    { id: '1', name: 'João Silva', status: 'active', notifications: 0 },
    { id: '2', name: 'Maria Santos', status: 'vacation', notifications: 1 },
    { id: '3', name: 'Pedro Costa', status: 'active', notifications: 2 },
    { id: '4', name: 'Ana Oliveira', status: 'leave', notifications: 0 },
    { id: '5', name: 'Carlos Lima', status: 'terminated', notifications: 0 },
    { id: '6', name: 'Julia Ferreira', status: 'active', notifications: 1 },
    { id: '7', name: 'Roberto Alves', status: 'active', notifications: 0 },
    { id: '8', name: 'Lucia Pereira', status: 'vacation', notifications: 0 },
  ];

  // Pulse animation
  useEffect(() => {
    const interval = setInterval(() => {
      setPulse(prev => prev + 1);
    }, 50);
    return () => clearInterval(interval);
  }, []);

  const handleRiverClick = (river: ClientRiver) => {
    setSelectedRiver(river);
    setViewMode('forest');
  };

  const handleHeartClick = () => {
    setViewMode('biome');
    setSelectedRiver(null);
  };

  const getEcosystemHealth = () => {
    const totalCompliance = clientRivers.reduce((sum, river) => sum + river.compliance, 0);
    const averageCompliance = totalCompliance / clientRivers.length;
    
    if (averageCompliance >= 80) return { color: 'success', text: 'Ecossistema Saudável' };
    if (averageCompliance >= 60) return { color: 'warning', text: 'Atenção Necessária' };
    return { color: 'error', text: 'Intervenção Crítica' };
  };

  const ecosystemHealth = getEcosystemHealth();

  return (
    <Box sx={{ height: '100vh', width: '100vw', position: 'relative', bgcolor: '#0a0a0a' }}>
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
          onClick={onBackToTraditional}
          sx={{ color: 'white', bgcolor: 'rgba(255,255,255,0.1)' }}
        >
          Voltar ao Dashboard Tradicional
        </Button>
        
        <Typography variant="h4" sx={{ color: 'white', fontWeight: 'bold' }}>
          🌱 KAIRÓS - Bioma Operacional
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Tooltip title="Dura Lex - Consciência Jurídica">
            <IconButton sx={{ color: '#4ecdc4' }}>
              <Psychology />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>

      {/* Ecosystem Health Alert */}
      <Alert
        severity={ecosystemHealth.color as any}
        sx={{
          position: 'absolute',
          top: 80,
          left: 16,
          zIndex: 10,
          bgcolor: 'rgba(255,255,255,0.9)',
        }}
      >
        <strong>{ecosystemHealth.text}</strong> - {clientRivers.length} rios ativos
      </Alert>

      {/* View Mode Controls */}
      <Box
        sx={{
          position: 'absolute',
          top: 80,
          right: 16,
          zIndex: 10,
          display: 'flex',
          gap: 1,
        }}
      >
        <Fab
          size="small"
          color={viewMode === 'biome' ? 'primary' : 'default'}
          onClick={() => setViewMode('biome')}
        >
          <Favorite />
        </Fab>
        {selectedRiver && (
          <Fab
            size="small"
            color={viewMode === 'forest' ? 'primary' : 'default'}
            onClick={() => setViewMode('forest')}
          >
            <Forest />
          </Fab>
        )}
      </Box>

      {/* 3D Canvas */}
      <Canvas
        camera={{ position: [0, 5, 10], fov: 75 }}
        style={{ width: '100%', height: '100%' }}
      >
        <ambientLight intensity={0.4} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        <pointLight position={[-10, -10, -10]} intensity={0.5} />
        
        {viewMode === 'biome' ? (
          // Biome View - Heart and Rivers
          <>
            <PulsingHeart pulse={pulse} onClick={handleHeartClick} />
            {clientRivers.map((river, index) => (
              <ClientRiver
                key={river.id}
                river={river}
                index={index}
                onRiverClick={handleRiverClick}
              />
            ))}
          </>
        ) : (
          // Forest View - Employee Trees
          <>
            {mockEmployees.map((employee, index) => {
              const x = (index % 4) * 3 - 4.5;
              const z = Math.floor(index / 4) * 3 - 3;
              return (
                <EmployeeTree
                  key={employee.id}
                  employee={employee}
                  position={[x, 0, z]}
                />
              );
            })}
            
            {/* Forest ground */}
            <mesh position={[0, -1, 0]} rotation={[-Math.PI / 2, 0, 0]}>
              <planeGeometry args={[20, 20]} />
              <meshPhongMaterial color="#2E7D32" opacity={0.7} transparent />
            </mesh>
          </>
        )}
        
        <OrbitControls enablePan={true} enableZoom={true} enableRotate={true} />
      </Canvas>

      {/* Bottom Info Panel */}
      {viewMode === 'forest' && selectedRiver && (
        <Paper
          sx={{
            position: 'absolute',
            bottom: 16,
            left: 16,
            right: 16,
            p: 2,
            bgcolor: 'rgba(255,255,255,0.95)',
            backdropFilter: 'blur(10px)',
          }}
        >
          <Typography variant="h6" gutterBottom>
            🌳 Floresta: {selectedRiver.name}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {mockEmployees.length} colaboradores visualizados • 
            Compliance: {selectedRiver.compliance}% • 
            Status: {selectedRiver.healthStatus === 'healthy' ? 'Saudável' : 
                    selectedRiver.healthStatus === 'warning' ? 'Atenção' : 'Crítico'}
          </Typography>
        </Paper>
      )}
    </Box>
  );
};

export default KairosOrganicDashboard;