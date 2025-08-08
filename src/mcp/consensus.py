"""
MCP Consensus Engine for AUDITORIA360
=====================================

Implementation of the consensus mechanism that requires quorum of multiple agents
before finalizing critical insights, as specified in "Grande Síntese" - Initiative IV.
"""

import asyncio
import logging
import time
import uuid
from collections import defaultdict
from datetime import datetime
from typing import Dict, List

from .protocol import (
    AgentRole,
    ConsensusLevel,
    ConsensusResult,
    ConsensusVote,
    MCPConsensusRequest,
)

logger = logging.getLogger(__name__)


class ConsensusAgent:
    """Individual agent participating in consensus"""

    def __init__(self, agent_id: str, role: AgentRole, confidence_base: float = 0.8):
        self.agent_id = agent_id
        self.role = role
        self.confidence_base = confidence_base
        self.active = True
        self.last_seen = datetime.now()

    async def evaluate_insight(
        self, insight_data: Dict, context: Dict = None
    ) -> ConsensusVote:
        """Evaluate an insight and return a vote"""
        # Simulate agent evaluation (replace with actual AI/rule-based logic)
        await asyncio.sleep(0.1)  # Simulate processing time

        # Role-specific evaluation logic
        vote, confidence, reasoning = self._role_specific_evaluation(
            insight_data, context
        )

        return ConsensusVote(
            agent_id=self.agent_id,
            agent_role=self.role,
            vote=vote,
            confidence=confidence,
            reasoning=reasoning,
            timestamp=datetime.now(),
            supporting_data=self._generate_supporting_data(insight_data),
        )

    def _role_specific_evaluation(
        self, insight_data: Dict, context: Dict = None
    ) -> tuple:
        """Role-specific evaluation logic"""
        insight_type = insight_data.get("type", "unknown")

        if self.role == AgentRole.SECURITY_AGENT:
            return self._security_evaluation(insight_data, context)
        elif self.role == AgentRole.RISK_AGENT:
            return self._risk_evaluation(insight_data, context)
        elif self.role == AgentRole.COMPLIANCE_AGENT:
            return self._compliance_evaluation(insight_data, context)
        elif self.role == AgentRole.AUDIT_AGENT:
            return self._audit_evaluation(insight_data, context)
        elif self.role == AgentRole.VALIDATION_AGENT:
            return self._validation_evaluation(insight_data, context)
        elif self.role == AgentRole.BUSINESS_AGENT:
            return self._business_evaluation(insight_data, context)
        else:
            return True, self.confidence_base, "Default approval by generic agent"

    def _security_evaluation(self, insight_data: Dict, context: Dict = None) -> tuple:
        """Security agent evaluation"""
        # Check for security-related concerns
        security_score = insight_data.get("security_score", 0.5)

        if security_score < 0.3:
            return (
                False,
                0.9,
                "Security score too low - potential security threat detected",
            )
        elif security_score < 0.6:
            return (
                False,
                0.7,
                "Security concerns identified - requires additional validation",
            )
        else:
            return True, min(security_score + 0.1, 1.0), "Security evaluation passed"

    def _risk_evaluation(self, insight_data: Dict, context: Dict = None) -> tuple:
        """Risk agent evaluation"""
        risk_level = insight_data.get("risk_level", "medium")

        if risk_level == "critical":
            return (
                False,
                0.95,
                "Critical risk level detected - requires immediate mitigation",
            )
        elif risk_level == "high":
            return False, 0.8, "High risk level - additional controls needed"
        elif risk_level == "medium":
            return True, 0.6, "Medium risk acceptable with monitoring"
        else:
            return True, 0.9, "Low risk - approved"

    def _compliance_evaluation(self, insight_data: Dict, context: Dict = None) -> tuple:
        """Compliance agent evaluation"""
        compliance_flags = insight_data.get("compliance_flags", [])

        if any("violation" in flag.lower() for flag in compliance_flags):
            return (
                False,
                0.95,
                f"Compliance violations detected: {', '.join(compliance_flags)}",
            )
        elif compliance_flags:
            return (
                True,
                0.7,
                f"Compliance flags noted but acceptable: {', '.join(compliance_flags)}",
            )
        else:
            return True, 0.85, "No compliance issues identified"

    def _audit_evaluation(self, insight_data: Dict, context: Dict = None) -> tuple:
        """Audit agent evaluation"""
        audit_trail = insight_data.get("audit_trail", [])
        data_integrity = insight_data.get("data_integrity", True)

        if not data_integrity:
            return False, 0.9, "Data integrity issues detected in audit trail"
        elif len(audit_trail) < 3:
            return False, 0.7, "Insufficient audit trail for verification"
        else:
            return True, 0.8, "Audit trail complete and data integrity verified"

    def _validation_evaluation(self, insight_data: Dict, context: Dict = None) -> tuple:
        """Validation agent evaluation"""
        validation_score = insight_data.get("validation_score", 0.5)
        data_quality = insight_data.get("data_quality", "unknown")

        if validation_score < 0.4:
            return False, 0.8, "Validation score below acceptable threshold"
        elif data_quality == "poor":
            return False, 0.7, "Poor data quality detected"
        else:
            return True, min(validation_score + 0.2, 1.0), "Validation checks passed"

    def _business_evaluation(self, insight_data: Dict, context: Dict = None) -> tuple:
        """Business agent evaluation"""
        business_impact = insight_data.get("business_impact", "medium")
        roi_score = insight_data.get("roi_score", 0.5)

        if business_impact == "critical" and roi_score < 0.3:
            return False, 0.8, "Critical business impact with poor ROI"
        elif roi_score < 0.2:
            return False, 0.6, "Business ROI too low"
        else:
            return (
                True,
                min(roi_score + 0.3, 1.0),
                f"Business impact {business_impact} with acceptable ROI",
            )

    def _generate_supporting_data(self, insight_data: Dict) -> Dict:
        """Generate supporting data for the vote"""
        return {
            "agent_role": self.role.value,
            "evaluation_criteria": f"{self.role.value}_specific_rules",
            "processing_time_ms": 100,  # Simulated
            "data_points_analyzed": len(insight_data),
            "confidence_factors": [
                "data_quality",
                "historical_patterns",
                "rule_compliance",
            ],
        }


class MCPConsensusEngine:
    """
    Multi-agent consensus engine for critical decision making.
    Requires quorum of multiple agents before finalizing critical insights.
    """

    def __init__(self):
        self.agents: Dict[str, ConsensusAgent] = {}
        self.active_consensus_sessions: Dict[str, Dict] = {}
        self.consensus_history: List[ConsensusResult] = []
        self.debate_logs: Dict[str, List[str]] = defaultdict(list)

        # Initialize default agents
        self._initialize_default_agents()

    def _initialize_default_agents(self):
        """Initialize the default set of consensus agents"""
        default_agents = [
            ("security_001", AgentRole.SECURITY_AGENT, 0.85),
            ("risk_001", AgentRole.RISK_AGENT, 0.80),
            ("compliance_001", AgentRole.COMPLIANCE_AGENT, 0.90),
            ("audit_001", AgentRole.AUDIT_AGENT, 0.88),
            ("validation_001", AgentRole.VALIDATION_AGENT, 0.82),
            ("business_001", AgentRole.BUSINESS_AGENT, 0.75),
        ]

        for agent_id, role, confidence in default_agents:
            self.register_agent(agent_id, role, confidence)

        logger.info(
            f"🤝 Initialized MCP consensus engine with {len(self.agents)} agents"
        )

    def register_agent(
        self, agent_id: str, role: AgentRole, confidence_base: float = 0.8
    ):
        """Register a new consensus agent"""
        agent = ConsensusAgent(agent_id, role, confidence_base)
        self.agents[agent_id] = agent
        logger.info(f"🤖 Registered consensus agent: {agent_id} ({role.value})")

    def unregister_agent(self, agent_id: str):
        """Unregister a consensus agent"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            logger.info(f"🚫 Unregistered consensus agent: {agent_id}")

    async def request_consensus(self, request: MCPConsensusRequest) -> ConsensusResult:
        """
        Request consensus from multiple agents on a critical insight.
        Implements the core consensus mechanism as specified in Grande Síntese.
        """
        start_time = time.time()
        consensus_id = str(uuid.uuid4())

        logger.info(
            f"🗳️ Starting consensus session {consensus_id} for insight type: {request.insight_type}"
        )

        # Filter agents based on requirements
        participating_agents = self._select_participating_agents(
            request.required_agent_roles
        )

        if not participating_agents:
            raise ValueError("No eligible agents found for consensus")

        # Initialize debate log
        self.debate_logs[consensus_id] = [
            f"Consensus session started with {len(participating_agents)} agents",
            f"Required consensus level: {request.consensus_level_required.value}",
            f"Insight type: {request.insight_type}",
        ]

        # Collect votes from all participating agents
        votes = await self._collect_votes(participating_agents, request, consensus_id)

        # Analyze consensus result
        result = self._analyze_consensus(
            consensus_id, votes, request, start_time, participating_agents
        )

        # Log the result
        self.consensus_history.append(result)

        logger.info(
            f"🏁 Consensus session {consensus_id} completed: "
            f"{'APPROVED' if result.decision_approved else 'REJECTED'} "
            f"({result.votes_for}/{result.total_agents} votes)"
        )

        return result

    def _select_participating_agents(
        self, required_roles: List[AgentRole]
    ) -> List[ConsensusAgent]:
        """Select agents that can participate in the consensus"""
        if not required_roles:
            # If no specific roles required, use all active agents
            return [agent for agent in self.agents.values() if agent.active]
        else:
            # Use only agents with required roles
            selected = []
            for agent in self.agents.values():
                if agent.active and agent.role in required_roles:
                    selected.append(agent)
            return selected

    async def _collect_votes(
        self,
        agents: List[ConsensusAgent],
        request: MCPConsensusRequest,
        consensus_id: str,
    ) -> List[ConsensusVote]:
        """Collect votes from all participating agents"""
        vote_tasks = []

        for agent in agents:
            self.debate_logs[consensus_id].append(
                f"Requesting vote from {agent.agent_id} ({agent.role.value})"
            )
            task = agent.evaluate_insight(request.insight_data, request.context)
            vote_tasks.append(task)

        # Wait for all votes with timeout
        try:
            votes = await asyncio.wait_for(
                asyncio.gather(*vote_tasks), timeout=request.timeout_seconds
            )

            # Log votes in debate
            for vote in votes:
                self.debate_logs[consensus_id].append(
                    f"{vote.agent_id}: {'APPROVE' if vote.vote else 'REJECT'} "
                    f"(confidence: {vote.confidence:.2f}) - {vote.reasoning}"
                )

            return votes

        except asyncio.TimeoutError:
            logger.error(f"Consensus timeout for session {consensus_id}")
            self.debate_logs[consensus_id].append(
                "TIMEOUT: Not all agents responded in time"
            )
            raise

    def _analyze_consensus(
        self,
        consensus_id: str,
        votes: List[ConsensusVote],
        request: MCPConsensusRequest,
        start_time: float,
        participating_agents: List[ConsensusAgent],
    ) -> ConsensusResult:
        """Analyze votes and determine consensus result"""

        total_agents = len(participating_agents)
        votes_for = sum(1 for vote in votes if vote.vote)
        votes_against = sum(1 for vote in votes if not vote.vote)
        abstentions = total_agents - len(votes)  # Agents that didn't vote

        # Calculate consensus percentage
        if total_agents > 0:
            consensus_achieved = votes_for / total_agents
        else:
            consensus_achieved = 0.0

        # Determine if quorum is met and decision approved
        quorum_met = len(votes) >= (total_agents * 0.5)  # At least 50% participation

        # Check if consensus level is achieved
        required_thresholds = {
            ConsensusLevel.SIMPLE: 0.51,
            ConsensusLevel.MAJORITY: 0.66,
            ConsensusLevel.SUPERMAJORITY: 0.75,
            ConsensusLevel.UNANIMOUS: 1.0,
        }

        required_threshold = required_thresholds[request.consensus_level_required]
        decision_approved = quorum_met and consensus_achieved >= required_threshold

        # Generate final reasoning
        if not quorum_met:
            final_reasoning = (
                f"Quorum not met: only {len(votes)}/{total_agents} agents participated"
            )
        elif not decision_approved:
            final_reasoning = (
                f"Consensus not reached: {consensus_achieved:.1%} approval, "
                f"required {required_threshold:.1%} for {request.consensus_level_required.value}"
            )
        else:
            final_reasoning = (
                f"Consensus achieved: {consensus_achieved:.1%} approval "
                f"meets {request.consensus_level_required.value} requirement"
            )

        # Log final decision in debate
        self.debate_logs[consensus_id].extend(
            [
                f"Final tally: {votes_for} approve, {votes_against} reject, {abstentions} abstentions",
                f"Consensus achieved: {consensus_achieved:.1%}",
                f"Decision: {'APPROVED' if decision_approved else 'REJECTED'}",
                f"Reasoning: {final_reasoning}",
            ]
        )

        processing_time = int((time.time() - start_time) * 1000)

        return ConsensusResult(
            consensus_id=consensus_id,
            decision_approved=decision_approved,
            total_agents=total_agents,
            votes_for=votes_for,
            votes_against=votes_against,
            abstentions=abstentions,
            consensus_level_required=request.consensus_level_required,
            consensus_level_achieved=consensus_achieved,
            quorum_met=quorum_met,
            individual_votes=votes,
            debate_log=self.debate_logs[consensus_id].copy(),
            final_reasoning=final_reasoning,
            timestamp=datetime.now(),
            processing_time_ms=processing_time,
        )

    def get_consensus_statistics(self) -> Dict:
        """Get statistics about consensus sessions"""
        if not self.consensus_history:
            return {"message": "No consensus sessions completed yet"}

        total_sessions = len(self.consensus_history)
        approved_sessions = sum(
            1 for result in self.consensus_history if result.decision_approved
        )

        avg_consensus_level = (
            sum(result.consensus_level_achieved for result in self.consensus_history)
            / total_sessions
        )
        avg_processing_time = (
            sum(result.processing_time_ms for result in self.consensus_history)
            / total_sessions
        )

        return {
            "total_sessions": total_sessions,
            "approved_sessions": approved_sessions,
            "rejection_rate": (total_sessions - approved_sessions) / total_sessions,
            "average_consensus_level": round(avg_consensus_level, 3),
            "average_processing_time_ms": round(avg_processing_time, 2),
            "active_agents": len([a for a in self.agents.values() if a.active]),
            "total_agents": len(self.agents),
        }


# Global consensus engine instance
_consensus_engine = MCPConsensusEngine()


def get_consensus_engine() -> MCPConsensusEngine:
    """Get the global consensus engine instance"""
    return _consensus_engine


async def require_consensus(
    insight_type: str,
    insight_data: Dict,
    consensus_level: ConsensusLevel = ConsensusLevel.MAJORITY,
    required_roles: List[AgentRole] = None,
) -> ConsensusResult:
    """
    Convenience function to require consensus on a critical insight.
    This is the main entry point for the consensus mechanism.
    """
    request = MCPConsensusRequest(
        insight_id=str(uuid.uuid4()),
        insight_type=insight_type,
        insight_data=insight_data,
        consensus_level_required=consensus_level,
        required_agent_roles=required_roles or [],
        priority="high",
    )

    engine = get_consensus_engine()
    return await engine.request_consensus(request)
