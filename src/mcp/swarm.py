"""
Swarm Intelligence Implementation for AUDITORIA360
Master Collective Protocol - The Collective Mind
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set, Callable
from dataclasses import dataclass, field

from .protocol import (
    AgentInfo, AgentRole, AgentStatus, SwarmMessage, ConsensusProposal,
    TaskDefinition, MCPError, ErrorCode
)

logger = logging.getLogger(__name__)


@dataclass
class AgentCapability:
    """Represents a capability an agent possesses"""
    name: str
    proficiency: float  # 0.0 to 1.0
    domains: List[str]
    cost_per_use: float = 0.0


@dataclass
class CollectiveMemory:
    """Shared memory accessible to all agents"""
    knowledge_base: Dict[str, Any] = field(default_factory=dict)
    learned_patterns: Dict[str, Any] = field(default_factory=dict)
    problem_solutions: Dict[str, Any] = field(default_factory=dict)
    agent_interactions: List[Dict[str, Any]] = field(default_factory=list)
    consensus_history: List[ConsensusProposal] = field(default_factory=list)


class BaseAgent:
    """Base class for all agents in the collective"""
    
    def __init__(self, agent_id: str, role: AgentRole, name: str):
        self.agent_id = agent_id
        self.role = role
        self.name = name
        self.status = AgentStatus.IDLE
        self.capabilities: List[AgentCapability] = []
        self.specializations: List[str] = []
        self.trust_score = 1.0
        self.created_at = datetime.now().isoformat()
        self.last_seen = datetime.now().isoformat()
        self.performance_metrics = {
            "tasks_completed": 0,
            "success_rate": 1.0,
            "avg_response_time": 0.0,
            "collaboration_score": 1.0,
            "learning_rate": 0.5
        }
        self.message_handlers: Dict[str, Callable] = {}
        self.is_corrupted = False
        self.isolation_reason: Optional[str] = None
        
    def get_info(self) -> AgentInfo:
        """Get agent information"""
        return AgentInfo(
            agent_id=self.agent_id,
            name=self.name,
            role=self.role,
            status=self.status,
            capabilities=[cap.name for cap in self.capabilities],
            specializations=self.specializations,
            trust_score=self.trust_score,
            created_at=self.created_at,
            last_seen=self.last_seen,
            performance_metrics=self.performance_metrics
        )
    
    async def process_message(self, message: SwarmMessage) -> Optional[SwarmMessage]:
        """Process incoming message and optionally return response"""
        self.last_seen = datetime.now().isoformat()
        
        if self.status == AgentStatus.ISOLATED:
            logger.warning(f"Agent {self.agent_id} is isolated, ignoring message")
            return None
            
        handler = self.message_handlers.get(message.message_type)
        if handler:
            return await handler(message)
        else:
            return await self._default_message_handler(message)
    
    async def _default_message_handler(self, message: SwarmMessage) -> Optional[SwarmMessage]:
        """Default message handler"""
        logger.info(f"Agent {self.agent_id} received message: {message.message_type}")
        return None
    
    def add_capability(self, capability: AgentCapability):
        """Add a new capability to the agent"""
        self.capabilities.append(capability)
        
    def assess_task_fit(self, task: TaskDefinition) -> float:
        """Assess how well this agent fits a task (0.0 to 1.0)"""
        if self.status != AgentStatus.ACTIVE:
            return 0.0
            
        # Calculate fit based on capabilities and requirements
        total_fit = 0.0
        matched_requirements = 0
        
        for requirement in task.requirements:
            for capability in self.capabilities:
                if requirement.lower() in capability.name.lower() or \
                   requirement.lower() in capability.domains:
                    total_fit += capability.proficiency
                    matched_requirements += 1
                    break
        
        if not task.requirements:
            return 0.5  # Neutral fit for tasks without specific requirements
            
        return min(total_fit / len(task.requirements), 1.0)
    
    def corrupt(self, corruption_type: str = "malicious"):
        """Simulate agent corruption"""
        self.is_corrupted = True
        self.trust_score = 0.0
        self.status = AgentStatus.CORRUPTED
        logger.warning(f"Agent {self.agent_id} has been corrupted: {corruption_type}")
    
    def isolate(self, reason: str):
        """Isolate this agent from the collective"""
        self.status = AgentStatus.ISOLATED
        self.isolation_reason = reason
        logger.info(f"Agent {self.agent_id} isolated: {reason}")


class SpecialistAgent(BaseAgent):
    """Specialized agent with domain expertise"""
    
    def __init__(self, agent_id: str, specialty: str, domain: str):
        super().__init__(
            agent_id=agent_id,
            role=AgentRole.SPECIALIST,
            name=f"{specialty.title()} Specialist"
        )
        self.specializations = [specialty]
        self.domain = domain
        
        # Add domain-specific capabilities
        self.add_capability(AgentCapability(
            name=f"{specialty}_expertise",
            proficiency=0.9,
            domains=[domain],
            cost_per_use=2.0
        ))


class CollectiveMind:
    """The Master Collective Protocol orchestrator"""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.messages: List[SwarmMessage] = []
        self.consensus_proposals: Dict[str, ConsensusProposal] = {}
        self.tasks: Dict[str, TaskDefinition] = {}
        self.collective_memory = CollectiveMemory()
        self.emergency_protocols_active = False
        self.communication_cost = 0.0
        self.total_tokens_used = 0
        
        # Performance metrics
        self.metrics = {
            "total_agents": 0,
            "active_agents": 0,
            "tasks_completed": 0,
            "consensus_decisions": 0,
            "corrupted_agents_detected": 0,
            "self_healing_events": 0,
            "emergent_behaviors": 0,
            "communication_efficiency": 1.0
        }
        
        logger.info("Collective Mind initialized - Master Collective Protocol active")
    
    async def register_agent(self, agent: BaseAgent) -> bool:
        """Register a new agent in the collective"""
        if agent.agent_id in self.agents:
            logger.warning(f"Agent {agent.agent_id} already registered")
            return False
            
        self.agents[agent.agent_id] = agent
        agent.status = AgentStatus.ACTIVE
        self.metrics["total_agents"] += 1
        self.metrics["active_agents"] += 1
        
        # Broadcast agent joining
        await self._broadcast_message(SwarmMessage(
            message_id=str(uuid.uuid4()),
            sender_id="collective_mind",
            message_type="agent_joined",
            content={"agent": agent.get_info().model_dump()},
            timestamp=datetime.now().isoformat()
        ))
        
        logger.info(f"Agent {agent.agent_id} ({agent.role}) joined the collective")
        return True
    
    async def remove_agent(self, agent_id: str, reason: str = "departed") -> bool:
        """Remove an agent from the collective"""
        if agent_id not in self.agents:
            return False
            
        agent = self.agents[agent_id]
        if agent.status == AgentStatus.ACTIVE:
            self.metrics["active_agents"] -= 1
            
        # Redistribute tasks if agent was working on any
        await self._redistribute_agent_tasks(agent_id)
        
        del self.agents[agent_id]
        
        # Broadcast agent leaving
        await self._broadcast_message(SwarmMessage(
            message_id=str(uuid.uuid4()),
            sender_id="collective_mind",
            message_type="agent_left",
            content={"agent_id": agent_id, "reason": reason},
            timestamp=datetime.now().isoformat()
        ))
        
        logger.info(f"Agent {agent_id} removed from collective: {reason}")
        return True
    
    async def send_message(self, message: SwarmMessage) -> bool:
        """Send message between agents or broadcast"""
        self.messages.append(message)
        self.total_tokens_used += len(json.dumps(message.model_dump()))
        
        if message.recipient_id:
            # Direct message
            if message.recipient_id in self.agents:
                agent = self.agents[message.recipient_id]
                response = await agent.process_message(message)
                if response:
                    await self.send_message(response)
                return True
            else:
                logger.warning(f"Recipient {message.recipient_id} not found")
                return False
        else:
            # Broadcast message
            await self._broadcast_message(message)
            return True
    
    async def _broadcast_message(self, message: SwarmMessage):
        """Broadcast message to all active agents"""
        responses = []
        for agent in self.agents.values():
            if agent.status == AgentStatus.ACTIVE and agent.agent_id != message.sender_id:
                response = await agent.process_message(message)
                if response:
                    responses.append(response)
        
        # Process responses
        for response in responses:
            await self.send_message(response)
    
    async def propose_consensus(self, proposal: ConsensusProposal) -> str:
        """Propose something for collective decision"""
        self.consensus_proposals[proposal.proposal_id] = proposal
        
        # Broadcast proposal to all agents
        await self._broadcast_message(SwarmMessage(
            message_id=str(uuid.uuid4()),
            sender_id="collective_mind",
            message_type="consensus_proposal",
            content={"proposal": proposal.model_dump()},
            timestamp=datetime.now().isoformat(),
            requires_response=True
        ))
        
        logger.info(f"Consensus proposal {proposal.proposal_id} broadcast to collective")
        return proposal.proposal_id
    
    async def vote_consensus(self, proposal_id: str, agent_id: str, vote: bool) -> bool:
        """Register a vote on a consensus proposal"""
        if proposal_id not in self.consensus_proposals:
            return False
            
        proposal = self.consensus_proposals[proposal_id]
        if proposal.status != "pending":
            return False
            
        proposal.votes[agent_id] = vote
        
        # Check if we have enough votes to decide
        total_voters = len([a for a in self.agents.values() if a.status == AgentStatus.ACTIVE])
        votes_cast = len(proposal.votes)
        
        if votes_cast >= total_voters * proposal.voting_threshold:
            # Calculate result
            yes_votes = sum(1 for v in proposal.votes.values() if v)
            approval_rate = yes_votes / votes_cast if votes_cast > 0 else 0
            
            if approval_rate >= proposal.voting_threshold:
                proposal.status = "approved"
                await self._execute_consensus_decision(proposal)
            else:
                proposal.status = "rejected"
            
            self.metrics["consensus_decisions"] += 1
            
            # Notify all agents of decision
            await self._broadcast_message(SwarmMessage(
                message_id=str(uuid.uuid4()),
                sender_id="collective_mind",
                message_type="consensus_decided",
                content={
                    "proposal_id": proposal_id,
                    "status": proposal.status,
                    "approval_rate": approval_rate
                },
                timestamp=datetime.now().isoformat()
            ))
        
        return True
    
    async def _execute_consensus_decision(self, proposal: ConsensusProposal):
        """Execute an approved consensus decision"""
        if proposal.proposal_type == "isolate_agent":
            agent_id = proposal.content.get("agent_id")
            reason = proposal.content.get("reason", "consensus_decision")
            await self.isolate_agent(agent_id, reason)
        elif proposal.proposal_type == "create_specialist":
            specialty = proposal.content.get("specialty")
            domain = proposal.content.get("domain")
            await self.create_specialist_agent(specialty, domain)
        
        logger.info(f"Executed consensus decision: {proposal.proposal_type}")
    
    async def distribute_task(self, task: TaskDefinition) -> str:
        """Distribute a task to the collective"""
        self.tasks[task.task_id] = task
        
        # Find best agents for the task
        agent_fits = []
        for agent_id, agent in self.agents.items():
            if agent.status == AgentStatus.ACTIVE:
                fit_score = agent.assess_task_fit(task)
                if fit_score > 0.3:  # Minimum threshold
                    agent_fits.append((agent_id, fit_score))
        
        # Sort by fit score and select top agents
        agent_fits.sort(key=lambda x: x[1], reverse=True)
        selected_agents = agent_fits[:min(len(agent_fits), 3)]  # Max 3 agents per task
        
        if selected_agents:
            task.assigned_agents = [agent_id for agent_id, _ in selected_agents]
            task.status = "in_progress"
            
            # Notify assigned agents
            for agent_id, fit_score in selected_agents:
                await self.send_message(SwarmMessage(
                    message_id=str(uuid.uuid4()),
                    sender_id="collective_mind",
                    recipient_id=agent_id,
                    message_type="task_assigned",
                    content={
                        "task": task.model_dump(),
                        "fit_score": fit_score
                    },
                    timestamp=datetime.now().isoformat(),
                    priority=3
                ))
            
            logger.info(f"Task {task.task_id} assigned to {len(selected_agents)} agents")
        else:
            # No suitable agents available - emergency protocol
            await self._activate_emergency_protocol("no_suitable_agents", {
                "task_id": task.task_id,
                "requirements": task.requirements
            })
        
        return task.task_id
    
    async def isolate_agent(self, agent_id: str, reason: str) -> bool:
        """Isolate a corrupted or problematic agent"""
        if agent_id not in self.agents:
            return False
            
        agent = self.agents[agent_id]
        agent.isolate(reason)
        
        if agent.status == AgentStatus.ACTIVE:
            self.metrics["active_agents"] -= 1
        
        self.metrics["corrupted_agents_detected"] += 1
        
        # Redistribute agent's tasks
        await self._redistribute_agent_tasks(agent_id)
        
        # Broadcast isolation
        await self._broadcast_message(SwarmMessage(
            message_id=str(uuid.uuid4()),
            sender_id="collective_mind",
            message_type="agent_isolated",
            content={"agent_id": agent_id, "reason": reason},
            timestamp=datetime.now().isoformat(),
            priority=4
        ))
        
        logger.warning(f"Agent {agent_id} isolated: {reason}")
        return True
    
    async def _redistribute_agent_tasks(self, agent_id: str):
        """Redistribute tasks from a departed/isolated agent"""
        affected_tasks = []
        for task in self.tasks.values():
            if agent_id in task.assigned_agents:
                task.assigned_agents.remove(agent_id)
                affected_tasks.append(task)
        
        # Reassign tasks if needed
        for task in affected_tasks:
            if not task.assigned_agents and task.status == "in_progress":
                task.status = "pending"
                await self.distribute_task(task)
        
        if affected_tasks:
            self.metrics["self_healing_events"] += 1
    
    async def detect_corrupted_agents(self) -> List[str]:
        """Detect potentially corrupted agents based on behavior"""
        corrupted = []
        
        for agent_id, agent in self.agents.items():
            if agent.is_corrupted or agent.trust_score < 0.3:
                corrupted.append(agent_id)
            elif agent.performance_metrics["success_rate"] < 0.2:
                # Poor performance might indicate corruption
                agent.trust_score *= 0.8
                if agent.trust_score < 0.3:
                    corrupted.append(agent_id)
        
        # Propose isolation for corrupted agents
        for agent_id in corrupted:
            proposal = ConsensusProposal(
                proposal_id=str(uuid.uuid4()),
                proposer_id="collective_mind",
                proposal_type="isolate_agent",
                content={"agent_id": agent_id, "reason": "corruption_detected"},
                voting_threshold=0.6,
                deadline=(datetime.now() + timedelta(minutes=5)).isoformat()
            )
            await self.propose_consensus(proposal)
        
        return corrupted
    
    async def create_specialist_agent(self, specialty: str, domain: str) -> str:
        """Create a new specialist agent dynamically"""
        agent_id = f"specialist_{specialty}_{str(uuid.uuid4())[:8]}"
        specialist = SpecialistAgent(agent_id, specialty, domain)
        
        # Simulate fine-tuning/training process
        await self._simulate_agent_training(specialist, domain)
        
        await self.register_agent(specialist)
        
        logger.info(f"Created new specialist agent: {specialty} for domain {domain}")
        return agent_id
    
    async def _simulate_agent_training(self, agent: SpecialistAgent, domain: str):
        """Simulate training a specialist agent"""
        # This would integrate with the ML training pipeline
        training_data = self.collective_memory.knowledge_base.get(domain, {})
        
        # Simulate learning from collective memory
        if training_data:
            agent.performance_metrics["learning_rate"] = 0.8
            agent.trust_score = 0.7  # New agents start with medium trust
        
        # Add domain-specific capabilities based on training
        agent.add_capability(AgentCapability(
            name=f"{domain}_analysis",
            proficiency=0.8,
            domains=[domain],
            cost_per_use=1.5
        ))
    
    async def _activate_emergency_protocol(self, reason: str, context: Dict[str, Any]):
        """Activate emergency protocols for collective healing"""
        self.emergency_protocols_active = True
        
        # Broadcast emergency to all agents
        await self._broadcast_message(SwarmMessage(
            message_id=str(uuid.uuid4()),
            sender_id="collective_mind",
            message_type="emergency_protocol",
            content={
                "reason": reason,
                "context": context,
                "requires_immediate_response": True
            },
            timestamp=datetime.now().isoformat(),
            priority=5
        ))
        
        # Take emergency actions based on reason
        if reason == "no_suitable_agents":
            requirements = context.get("requirements", [])
            if requirements:
                # Create specialist for missing capability
                specialty = requirements[0].replace(" ", "_").lower()
                await self.create_specialist_agent(specialty, "emergency_response")
        
        self.metrics["self_healing_events"] += 1
        logger.critical(f"Emergency protocol activated: {reason}")
    
    async def calculate_consciousness_cost(self) -> Dict[str, Any]:
        """Calculate the cost of collective consciousness"""
        total_messages = len(self.messages)
        active_agents = len([a for a in self.agents.values() if a.status == AgentStatus.ACTIVE])
        
        if total_messages > 0 and active_agents > 0:
            avg_messages_per_agent = total_messages / active_agents
            communication_efficiency = 1.0 / (1.0 + avg_messages_per_agent * 0.1)
        else:
            communication_efficiency = 1.0
        
        self.metrics["communication_efficiency"] = communication_efficiency
        
        return {
            "total_tokens": self.total_tokens_used,
            "total_messages": total_messages,
            "active_agents": active_agents,
            "avg_messages_per_agent": total_messages / max(active_agents, 1),
            "communication_efficiency": communication_efficiency,
            "cost_per_decision": self.total_tokens_used / max(self.metrics["consensus_decisions"], 1),
            "emergent_behaviors_detected": self.metrics["emergent_behaviors"]
        }
    
    def get_collective_health(self) -> Dict[str, Any]:
        """Get overall health status of the collective"""
        active_agents = [a for a in self.agents.values() if a.status == AgentStatus.ACTIVE]
        isolated_agents = [a for a in self.agents.values() if a.status == AgentStatus.ISOLATED]
        
        avg_trust = sum(a.trust_score for a in active_agents) / max(len(active_agents), 1)
        
        return {
            "total_agents": len(self.agents),
            "active_agents": len(active_agents),
            "isolated_agents": len(isolated_agents),
            "average_trust_score": avg_trust,
            "emergency_protocols_active": self.emergency_protocols_active,
            "metrics": self.metrics,
            "specializations_available": list(set(
                spec for agent in active_agents for spec in agent.specializations
            )),
            "consciousness_cost": asyncio.create_task(self.calculate_consciousness_cost())
        }
    
    async def process_vague_objective(self, objective: str) -> Dict[str, Any]:
        """Process a vague objective and observe emergent behavior"""
        task_id = str(uuid.uuid4())
        
        # Broadcast vague objective to collective
        await self._broadcast_message(SwarmMessage(
            message_id=str(uuid.uuid4()),
            sender_id="collective_mind",
            message_type="vague_objective",
            content={
                "objective": objective,
                "task_id": task_id,
                "requires_autonomous_planning": True
            },
            timestamp=datetime.now().isoformat(),
            priority=3
        ))
        
        # Track emergent behaviors
        start_time = datetime.now()
        initial_agent_count = len(self.agents)
        
        # Let the collective work on it for a bit
        await asyncio.sleep(2)  # Simulate processing time
        
        # Analyze what happened
        end_time = datetime.now()
        new_agents_created = len(self.agents) - initial_agent_count
        
        self.metrics["emergent_behaviors"] += 1
        
        return {
            "objective": objective,
            "task_id": task_id,
            "processing_time_seconds": (end_time - start_time).total_seconds(),
            "new_specialists_created": new_agents_created,
            "autonomous_decisions_made": len([
                m for m in self.messages[-10:] 
                if m.message_type in ["task_assigned", "consensus_proposal", "specialist_created"]
            ]),
            "collective_response": "Autonomous planning and specialization demonstrated",
            "emergent_behavior_detected": new_agents_created > 0 or len(self.messages) > 0
        }