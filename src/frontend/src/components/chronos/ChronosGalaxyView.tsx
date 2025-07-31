import React, { useRef, useMemo, useState } from 'react';
import { Canvas, useFrame, useThree, extend } from '@react-three/fiber';
import { Box, Typography, IconButton, Paper, Fade } from '@mui/material';
import { ArrowBack, Settings, Help } from '@mui/icons-material';
import * as THREE from 'three';

// Extend with OrbitControls
import { OrbitControls } from 'three-stdlib';
extend({ OrbitControls });

// Sample data representing accounting firms (contabilidades)
interface ContabilidadeData {
  id: string;
  name: string;
  position: [number, number, number];
  health: number; // 0-1, affects star brightness and color
  clientCount: number;
  errorCount: number;
  activity: number; // 0-1, affects pulsing
}

const mockContabilidades: ContabilidadeData[] = [
  {
    id: '1',
    name: 'ContaExcel Ltda',
    position: [5, 2, -3],
    health: 0.9,
    clientCount: 45,
    errorCount: 2,
    activity: 0.8
  },
  {
    id: '2', 
    name: 'Tributech Contadores',
    position: [-3, -1, 2],
    health: 0.7,
    clientCount: 67,
    errorCount: 8,
    activity: 0.6
  },
  {
    id: '3',
    name: 'NeoFiscal',
    position: [0, 4, -5],
    health: 0.95,
    clientCount: 23,
    errorCount: 0,
    activity: 0.9
  },
  {
    id: '4',
    name: 'Compliance 360',
    position: [-6, 0, 1],
    health: 0.5,
    clientCount: 89,
    errorCount: 15,
    activity: 0.3
  },
  {
    id: '5',
    name: 'Digital Tax',
    position: [2, -3, 3],
    health: 0.85,
    clientCount: 34,
    errorCount: 3,
    activity: 0.7
  }
];

// Simple HTML overlay for info
function InfoOverlay({ data, position }: { data: ContabilidadeData; position: [number, number, number] }) {
  return (
    <div 
      style={{
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        background: 'rgba(0, 0, 0, 0.8)',
        color: 'white',
        padding: '8px',
        borderRadius: '4px',
        minWidth: '200px',
        fontSize: '12px',
        pointerEvents: 'none',
        zIndex: 1000
      }}
    >
      <Typography variant="subtitle1">{data.name}</Typography>
      <Typography variant="body2">Clientes: {data.clientCount}</Typography>
      <Typography variant="body2">Erros: {data.errorCount}</Typography>
      <Typography variant="body2">
        Saúde: {(data.health * 100).toFixed(0)}%
      </Typography>
    </div>
  );
}

// Individual star component representing a contabilidade
function ContabilidadeStar({ 
  data, 
  onClick, 
  isSelected,
  onHover 
}: { 
  data: ContabilidadeData; 
  onClick: (data: ContabilidadeData) => void;
  isSelected: boolean;
  onHover: (data: ContabilidadeData | null) => void;
}) {
  const meshRef = useRef<THREE.Mesh>(null);

  // Animate the star with pulsing based on activity
  useFrame((state) => {
    if (meshRef.current) {
      const time = state.clock.getElapsedTime();
      const pulse = 1 + Math.sin(time * data.activity * 5) * 0.2;
      meshRef.current.scale.setScalar(pulse * (isSelected ? 1.5 : 1));
      
      // Gentle rotation
      meshRef.current.rotation.y += 0.005 * data.activity;
    }
  });

  // Calculate color based on health
  const starColor = useMemo(() => {
    if (data.health > 0.8) return new THREE.Color(0.3, 1, 0.3); // Green - healthy
    if (data.health > 0.6) return new THREE.Color(1, 1, 0.3); // Yellow - warning
    return new THREE.Color(1, 0.3, 0.3); // Red - critical
  }, [data.health]);

  return (
    <group position={data.position}>
      <mesh
        ref={meshRef}
        onClick={() => onClick(data)}
        onPointerOver={() => onHover(data)}
        onPointerOut={() => onHover(null)}
      >
        <sphereGeometry args={[0.3, 8, 8]} />
        <meshBasicMaterial 
          color={starColor} 
          transparent 
          opacity={0.7 + data.health * 0.3}
        />
      </mesh>
      
      {/* Glow effect */}
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[0.5, 8, 8]} />
        <meshBasicMaterial 
          color={starColor} 
          transparent 
          opacity={0.1} 
        />
      </mesh>
    </group>
  );
}

// Background starfield
function Starfield() {
  const starsRef = useRef<THREE.Points>(null);
  
  const starPositions = useMemo(() => {
    const positions = [];
    for (let i = 0; i < 1000; i++) {
      positions.push(
        (Math.random() - 0.5) * 100,
        (Math.random() - 0.5) * 100,
        (Math.random() - 0.5) * 100
      );
    }
    return new Float32Array(positions);
  }, []);

  useFrame(() => {
    if (starsRef.current) {
      starsRef.current.rotation.y += 0.0005;
    }
  });

  return (
    <points ref={starsRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={starPositions.length / 3}
          array={starPositions}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial size={0.05} color={0xffffff} transparent opacity={0.6} />
    </points>
  );
}

// Camera controller for smooth navigation  
function CameraController() {
  const { camera, gl } = useThree();
  const controlsRef = useRef();
  
  useFrame(() => {
    if (controlsRef.current) {
      (controlsRef.current as any).update();
    }
  });

  return (
    // @ts-ignore
    <orbitControls
      ref={controlsRef}
      args={[camera, gl.domElement]}
      enablePan={true}
      enableZoom={true}
      enableRotate={true}
      zoomSpeed={0.6}
      panSpeed={0.8}
      rotateSpeed={0.4}
    />
  );
}

interface ChronosGalaxyViewProps {
  onBackToTraditional: () => void;
}

const ChronosGalaxyView: React.FC<ChronosGalaxyViewProps> = ({ onBackToTraditional }) => {
  const [selectedStar, setSelectedStar] = useState<ContabilidadeData | null>(null);
  const [hoveredStar, setHoveredStar] = useState<ContabilidadeData | null>(null);
  const [showHelp, setShowHelp] = useState(false);

  const handleStarClick = (data: ContabilidadeData) => {
    setSelectedStar(data);
    console.log('Flying towards:', data.name);
    // TODO: Implement solar system view transition
  };

  return (
    <Box sx={{ height: '100vh', width: '100%', position: 'relative' }}>
      {/* Top control bar */}
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          zIndex: 1000,
          p: 2,
          background: 'linear-gradient(to bottom, rgba(0,0,0,0.7), transparent)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <IconButton 
            color="primary" 
            onClick={onBackToTraditional}
            sx={{ bgcolor: 'rgba(255,255,255,0.1)' }}
          >
            <ArrowBack />
          </IconButton>
          <Typography variant="h5" sx={{ color: 'white', fontWeight: 'bold' }}>
            CHRONOS - Visão do Observatório
          </Typography>
        </Box>

        <Box sx={{ display: 'flex', gap: 1 }}>
          <IconButton 
            color="primary"
            onClick={() => setShowHelp(!showHelp)}
            sx={{ bgcolor: 'rgba(255,255,255,0.1)' }}
          >
            <Help />
          </IconButton>
          <IconButton 
            color="primary"
            sx={{ bgcolor: 'rgba(255,255,255,0.1)' }}
          >
            <Settings />
          </IconButton>
        </Box>
      </Box>

      {/* Help panel */}
      <Fade in={showHelp}>
        <Paper
          sx={{
            position: 'absolute',
            top: 80,
            right: 16,
            zIndex: 1000,
            p: 2,
            maxWidth: 300,
            bgcolor: 'rgba(0,0,0,0.8)',
            color: 'white'
          }}
        >
          <Typography variant="h6" gutterBottom>Navegação Espacial</Typography>
          <Typography variant="body2" paragraph>
            • Cada estrela representa uma Contabilidade
          </Typography>
          <Typography variant="body2" paragraph>
            • Cor Verde: Saúde ótima (&gt;80%)
          </Typography>
          <Typography variant="body2" paragraph>
            • Cor Amarela: Atenção (60-80%)
          </Typography>
          <Typography variant="body2" paragraph>
            • Cor Vermelha: Crítico (&lt;60%)
          </Typography>
          <Typography variant="body2">
            • Clique em uma estrela para navegar ao sistema
          </Typography>
        </Paper>
      </Fade>

      {/* Hover info overlay */}
      {hoveredStar && (
        <div 
          style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            background: 'rgba(0, 0, 0, 0.8)',
            color: 'white',
            padding: '12px',
            borderRadius: '8px',
            minWidth: '200px',
            pointerEvents: 'none',
            zIndex: 1000
          }}
        >
          <Typography variant="h6">{hoveredStar.name}</Typography>
          <Typography variant="body2">Clientes: {hoveredStar.clientCount}</Typography>
          <Typography variant="body2">Erros: {hoveredStar.errorCount}</Typography>
          <Typography variant="body2">
            Saúde: {(hoveredStar.health * 100).toFixed(0)}%
          </Typography>
        </div>
      )}

      {/* Selected star info */}
      {selectedStar && (
        <Paper
          sx={{
            position: 'absolute',
            bottom: 16,
            left: 16,
            zIndex: 1000,
            p: 2,
            bgcolor: 'rgba(0,0,0,0.8)',
            color: 'white',
            minWidth: 250
          }}
        >
          <Typography variant="h6">{selectedStar.name}</Typography>
          <Typography variant="body2">Status: Sistema Selecionado</Typography>
          <Typography variant="body2">Preparando navegação...</Typography>
        </Paper>
      )}

      {/* 3D Canvas */}
      <Canvas
        camera={{ position: [0, 0, 10], fov: 75 }}
        style={{ background: 'linear-gradient(to bottom, #000011, #000033)' }}
      >
        <ambientLight intensity={0.1} />
        <pointLight position={[10, 10, 10]} intensity={0.5} />
        
        <Starfield />
        
        {mockContabilidades.map((contabilidade) => (
          <ContabilidadeStar
            key={contabilidade.id}
            data={contabilidade}
            onClick={handleStarClick}
            isSelected={selectedStar?.id === contabilidade.id}
            onHover={setHoveredStar}
          />
        ))}

        <CameraController />
      </Canvas>
    </Box>
  );
};

export default ChronosGalaxyView;