"""
PolicyMind AI OpenEnv Environment.
Real-world document decision environment for insurance claim processing.
"""

import asyncio
import json
import re
import random
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

from .models import (
    Observation, Action, Reward, EnvironmentState, DocumentSample, PolicyRule,
    ActionType, DocumentType, ExtractedField, MatchedRule, Decision, EvaluationResult
)


class PolicyMindEnvironment:
    """
    PolicyMind AI Environment for document-based decision making.
    
    This environment simulates real-world insurance claim processing where
    an AI agent must extract information, match policy rules, and make
    informed decisions.
    """
    
    def __init__(self, task_difficulty: str = "medium", max_steps: int = 10):
        self.task_difficulty = task_difficulty
        self.max_steps = max_steps
        self.current_step = 0
        self.current_document: Optional[DocumentSample] = None
        self.current_rules: List[PolicyRule] = []
        self._state: Optional[EnvironmentState] = None
        self.episode_history: List[Dict[str, Any]] = []
        
        # Initialize sample documents and rules
        self._initialize_documents()
        self._initialize_policy_rules()
    
    def _initialize_documents(self):
        """Initialize sample documents for the environment."""
        self.documents = {
            "insurance_claim_1": DocumentSample(
                document_id="insurance_claim_1",
                document_type=DocumentType.INSURANCE_CLAIM,
                title="Auto Insurance Claim - Vehicle Accident",
                content="""
                CLAIM INFORMATION
                Claim ID: CLM-2024-001234
                Policy Number: POL-2023-045678
                Date of Incident: 2024-03-15
                Claim Filed: 2024-03-16
                
                INSURED INFORMATION
                Name: John Michael Smith
                Age: 35
                License Number: DL123456789
                Address: 123 Main Street, Anytown, CA 90210
                
                VEHICLE INFORMATION
                Make: Toyota
                Model: Camry
                Year: 2021
                VIN: 1HGBH41JXMN109186
                License Plate: ABC123
                
                INCIDENT DETAILS
                Location: Highway 101, Mile Marker 45
                Time: 2:30 PM
                Weather: Clear
                Road Conditions: Dry
                
                DESCRIPTION OF INCIDENT:
                While driving northbound on Highway 101, another vehicle
                (Honda Civic, License: XYZ789) changed lanes abruptly and
                struck the driver's side of my vehicle. The impact caused
                significant damage to the driver's door and front fender.
                
                DAMAGES:
                - Driver's door: Complete replacement required
                - Front fender: Repair and repaint
                - Side mirror: Replacement
                - Labor: 8 hours estimated
                
                ESTIMATED COST: $4,250.00
                
                POLICE REPORT:
                Report Number: PR-2024-0315-789
                Officer: Officer Johnson, Badge #456
                Citation issued to other driver for improper lane change
                
                WITNESSES:
                - Jane Doe (555-0101), Vehicle behind
                - Bob Wilson (555-0102), Vehicle in adjacent lane
                
                MEDICAL INFORMATION:
                No injuries reported by insured party.
                Ambulance not called.
                """,
                ground_truth={
                    "extracted_fields": {
                        "claim_id": "CLM-2024-001234",
                        "policy_number": "POL-2023-045678",
                        "incident_date": "2024-03-15",
                        "insured_name": "John Michael Smith",
                        "insured_age": 35,
                        "vehicle_make": "Toyota",
                        "vehicle_model": "Camry",
                        "vehicle_year": 2021,
                        "estimated_cost": 4250.00,
                        "police_report_filed": True,
                        "injuries_reported": False
                    },
                    "applicable_rules": ["collision_coverage", "police_report_required", "no_fault_claim"],
                    "decision": "Approved",
                    "confidence": 0.85
                },
                difficulty="medium"
            ),
            
            "insurance_claim_2": DocumentSample(
                document_id="insurance_claim_2",
                document_type=DocumentType.INSURANCE_CLAIM,
                title="Home Insurance Claim - Water Damage",
                content="""
                CLAIM INFORMATION
                Claim ID: CLM-2024-005678
                Policy Number: POL-2022-098765
                Date of Incident: 2024-02-28
                Claim Filed: 2024-03-01
                
                INSURED INFORMATION
                Name: Sarah Johnson
                Age: 42
                Address: 456 Oak Avenue, Sometown, NY 10001
                Policy Type: Homeowner's Comprehensive
                
                PROPERTY INFORMATION
                Property Type: Single Family Home
                Year Built: 1998
                Square Feet: 2,150
                Construction: Wood Frame
                
                INCIDENT DETAILS
                Location: Kitchen area
                Time: Approximately 6:00 AM
                Cause: Burst water pipe under kitchen sink
                
                DESCRIPTION OF INCIDENT:
                Woke up to find water flowing from under kitchen sink.
                Water had spread to kitchen floor and was beginning to
                seep into adjacent dining room carpet. Main water supply
                was immediately shut off.
                
                DAMAGES:
                - Kitchen cabinets: Water damage, replacement needed
                - Kitchen flooring: Laminate warped, replacement needed
                - Dining room carpet: Water damage, cleaning required
                - Drywall: Minor damage near sink base
                - Personal property: Some items in lower cabinets damaged
                
                ESTIMATED COST: $12,750.00
                
                MITIGATION EFFORTS:
                - Water extracted immediately
                - Fans and dehumidifiers deployed
                - Professional water damage company contacted
                
                PRIOR CLAIMS:
                - 2022: Roof damage from storm (Approved)
                - 2023: Theft claim (Approved)
                
                INSURANCE ADJUSTER NOTES:
                Cause of loss appears to be sudden and accidental.
                No signs of neglect or maintenance issues.
                Policy covers sudden water damage.
                """,
                ground_truth={
                    "extracted_fields": {
                        "claim_id": "CLM-2024-005678",
                        "policy_number": "POL-2022-098765",
                        "incident_date": "2024-02-28",
                        "insured_name": "Sarah Johnson",
                        "insured_age": 42,
                        "property_type": "Single Family Home",
                        "incident_cause": "Burst water pipe",
                        "estimated_cost": 12750.00,
                        "prior_claims": 2,
                        "mitigation_efforts": True
                    },
                    "applicable_rules": ["sudden_accidental_damage", "water_damage_coverage", "maintenance_required"],
                    "decision": "Approved",
                    "confidence": 0.90
                },
                difficulty="medium"
            ),
            
            "policy_document_1": DocumentSample(
                document_id="policy_document_1",
                document_type=DocumentType.POLICY_DOCUMENT,
                title="Auto Insurance Policy - Comprehensive Coverage",
                content="""
                AUTO INSURANCE POLICY
                Policy Number: POL-TEMPLATE-001
                Effective Date: 2024-01-01
                
                COVERAGE SECTIONS:
                
                SECTION A - LIABILITY COVERAGE
                Bodily Injury Liability: $50,000 per person / $100,000 per accident
                Property Damage Liability: $25,000 per accident
                
                SECTION B - MEDICAL PAYMENTS
                Medical Expenses Coverage: $5,000 per person
                Funeral Expenses: $2,000 per person
                
                SECTION C - UNINSURED MOTORIST
                Uninsured Motorist Bodily Injury: $50,000 per person / $100,000 per accident
                
                SECTION D - PHYSICAL DAMAGE
                Collision Coverage: Actual Cash Value with $500 deductible
                Comprehensive Coverage: Actual Cash Value with $250 deductible
                
                POLICY CONDITIONS:
                
                1. DUTY TO NOTIFY
                The insured must notify the company of any accident or loss
                as soon as reasonably possible. Written notice must be provided
                within 30 days of the incident.
                
                2. COOPERATION CLAUSE
                The insured must cooperate with the company in the investigation,
                settlement, or defense of any claim or suit.
                
                3. POLICE REPORT REQUIREMENT
                For any accident involving property damage exceeding $1,000
                or bodily injury, a police report must be filed and provided
                to the insurance company.
                
                4. MAINTENANCE REQUIREMENTS
                The insured must maintain the vehicle in good working condition.
                Claims may be denied if loss results from lack of maintenance.
                
                5. FRAUD PROVISION
                Any intentional misrepresentation or concealment of material facts
                may result in claim denial and policy cancellation.
                
                EXCLUSIONS:
                
                - Intentional damage by insured
                - Racing or speed competitions
                - Using vehicle for commercial purposes
                - Driving under the influence
                - Mechanical breakdown (not resulting from accident)
                - Wear and tear
                
                CLAIM PROCESS:
                
                1. Report incident within 24 hours
                2. Submit claim form within 30 days
                3. Provide documentation (photos, estimates, police report)
                4. Vehicle inspection by adjuster
                5. Repair authorization
                6. Payment processing
                """,
                ground_truth={
                    "extracted_fields": {
                        "policy_type": "Auto Insurance",
                        "liability_limit": 100000,
                        "collision_deductible": 500,
                        "comprehensive_deductible": 250,
                        "police_report_threshold": 1000,
                        "notification_period_days": 30
                    },
                    "applicable_rules": ["liability_coverage", "police_report_required", "maintenance_required"],
                    "decision": "N/A",
                    "confidence": 0.0
                },
                difficulty="easy"
            )
        }
    
    def _initialize_policy_rules(self):
        """Initialize policy rules for the environment."""
        self.policy_rules = [
            PolicyRule(
                rule_id="collision_coverage",
                category="coverage",
                title="Collision Coverage Rule",
                description="Covers damage to vehicle from collision with another vehicle or object",
                conditions=[
                    "Vehicle damage from collision",
                    "Policy includes collision coverage",
                    "Deductible applies to claim"
                ],
                actions=[
                    "Verify policy has collision coverage",
                    "Apply deductible to claim amount",
                    "Assess fault if applicable"
                ],
                priority=3
            ),
            
            PolicyRule(
                rule_id="police_report_required",
                category="documentation",
                title="Police Report Requirement",
                description="Police report required for accidents exceeding damage threshold",
                conditions=[
                    "Property damage exceeds $1,000",
                    "Bodily injury occurred",
                    "Accident involved multiple vehicles"
                ],
                actions=[
                    "Request police report from insured",
                    "Verify report authenticity",
                    "Check report matches claim details"
                ],
                priority=4
            ),
            
            PolicyRule(
                rule_id="sudden_accidental_damage",
                category="coverage",
                title="Sudden and Accidental Damage",
                description="Covers sudden and accidental damage to property",
                conditions=[
                    "Damage was sudden, not gradual",
                    "Damage was accidental, not intentional",
                    "No neglect or maintenance issues"
                ],
                actions=[
                    "Verify timing of damage discovery",
                    "Check for signs of prior damage",
                    "Assess maintenance history"
                ],
                priority=3
            ),
            
            PolicyRule(
                rule_id="water_damage_coverage",
                category="coverage",
                title="Water Damage Coverage",
                description="Covers sudden water damage from covered perils",
                conditions=[
                    "Water damage is sudden and accidental",
                    "Source is covered (burst pipe, appliance failure)",
                    "No neglect in maintenance"
                ],
                actions=[
                    "Identify water source",
                    "Verify sudden vs gradual damage",
                    "Check for maintenance neglect"
                ],
                priority=2
            ),
            
            PolicyRule(
                rule_id="maintenance_required",
                category="conditions",
                title="Maintenance Requirements",
                description="Insured must maintain property in good condition",
                conditions=[
                    "Regular maintenance performed",
                    "No obvious neglect",
                    "Property age considered reasonable"
                ],
                actions=[
                    "Review maintenance records",
                    "Inspect for neglect signs",
                    "Consider property age and condition"
                ],
                priority=2
            ),
            
            PolicyRule(
                rule_id="no_fault_claim",
                category="liability",
                title="No-Fault Claim Processing",
                description="Process claims where insured is not at fault",
                conditions=[
                    "Other party at fault",
                    "Police report or evidence available",
                    "Other party insurance information available"
                ],
                actions=[
                    "Verify other party fault",
                    "Contact other insurance company",
                    "Process as subrogation claim"
                ],
                priority=1
            )
        ]
    
    async def reset(self, task_difficulty: Optional[str] = None) -> Observation:
        """
        Reset the environment for a new episode.
        
        Args:
            task_difficulty: Optional difficulty override
            
        Returns:
            Initial observation
        """
        if task_difficulty:
            self.task_difficulty = task_difficulty
        
        self.current_step = 0
        self.episode_history = []
        
        # Select document based on difficulty
        if self.task_difficulty == "easy":
            doc_id = "policy_document_1"
        elif self.task_difficulty == "medium":
            doc_id = random.choice(["insurance_claim_1", "insurance_claim_2"])
        else:  # hard
            doc_id = random.choice(["insurance_claim_1", "insurance_claim_2"])
        
        self.current_document = self.documents[doc_id]
        
        # Select relevant rules based on document type
        if self.current_document.document_type == DocumentType.INSURANCE_CLAIM:
            self.current_rules = [rule for rule in self.policy_rules 
                                if rule.category in ["coverage", "documentation", "conditions", "liability"]]
        else:
            self.current_rules = [rule for rule in self.policy_rules 
                                if rule.category in ["coverage", "documentation", "conditions"]]
        
        # Create initial observation
        observation = Observation(
            step=self.current_step,
            max_steps=self.max_steps,
            document_type=self.current_document.document_type,
            document_text=self.current_document.content,
            policy_rules=[rule.description for rule in self.current_rules],
            task_type=self.task_difficulty,
            hints=self._get_task_hints()
        )
        
        self._state = EnvironmentState(
            observation=observation,
            action_count=0,
            episode_complete=False
        )
        
        return observation
    
    def _get_task_hints(self) -> List[str]:
        """Get hints based on current task difficulty."""
        if self.task_difficulty == "easy":
            return [
                "Focus on extracting key numerical values and identifiers",
                "Look for claim IDs, policy numbers, dates, and amounts",
                "Return results in JSON format"
            ]
        elif self.task_difficulty == "medium":
            return [
                "Match document content to relevant policy rules",
                "Identify which conditions are met",
                "Consider the priority of different rules"
            ]
        else:  # hard
            return [
                "Make a final decision based on all available information",
                "Provide clear justification for your decision",
                "Consider confidence and risk factors"
            ]
    
    async def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict[str, Any]]:
        """
        Execute one step in the environment.
        
        Args:
            action: Action to execute
            
        Returns:
            Tuple of (observation, reward, done, info)
        """
        if self._state is None:
            raise RuntimeError("Environment not reset. Call reset() first.")
        
        self.current_step += 1
        self._state.action_count += 1
        
        # Execute action and calculate reward
        step_reward, reward_components, penalties, bonuses = await self._execute_action(action)
        
        # Update observation
        observation = await self._update_observation(action)
        
        # Check if episode is complete
        done = await self._check_episode_completion(action)
        
        # Create reward object
        reward = Reward(
            total_reward=step_reward,
            step_reward=step_reward,
            component_rewards=reward_components,
            penalties=penalties,
            bonuses=bonuses
        )
        
        # Update state
        self._state.observation = observation
        self._state.episode_complete = done
        
        if done:
            self._state.final_score = await self._calculate_final_score()
        
        # Record action in history
        self.episode_history.append({
            "step": self.current_step,
            "action": action.dict(),
            "reward": step_reward,
            "observation": observation.dict()
        })
        
        info = {
            "step": self.current_step,
            "action_count": self._state.action_count,
            "final_score": self._state.final_score if done else None
        }
        
        return observation, reward, done, info
    
    async def _execute_action(self, action: Action) -> Tuple[float, Dict[str, float], List[str], List[str]]:
        """Execute the action and return reward components."""
        step_reward = 0.0
        reward_components = {}
        penalties = []
        bonuses = []
        
        try:
            if action.action_type == ActionType.EXTRACT:
                reward, components = await self._handle_extraction(action)
                reward_components.update(components)
                step_reward += reward
                
            elif action.action_type == ActionType.MATCH_RULES:
                reward, components = await self._handle_rule_matching(action)
                reward_components.update(components)
                step_reward += reward
                
            elif action.action_type == ActionType.MAKE_DECISION:
                reward, components = await self._handle_decision(action)
                reward_components.update(components)
                step_reward += reward
                
            elif action.action_type == ActionType.QUERY:
                reward, components = await self._handle_query(action)
                reward_components.update(components)
                step_reward += reward
            
            # Check for penalties
            if self.current_step > self.max_steps:
                penalties.append("Exceeded maximum steps")
                step_reward -= 0.5
            
            # Bonus for efficiency
            if self.current_step <= self.max_steps * 0.7:
                bonuses.append("Efficient completion")
                step_reward += 0.1
                
        except Exception as e:
            penalties.append(f"Action execution failed: {str(e)}")
            step_reward -= 0.2
        
        return step_reward, reward_components, penalties, bonuses
    
    async def _handle_extraction(self, action: Action) -> Tuple[float, Dict[str, float]]:
        """Handle field extraction action."""
        if not action.extraction_fields:
            return 0.0, {}
        
        ground_truth = self.current_document.ground_truth.get("extracted_fields", {})
        extracted_count = 0
        total_fields = len(action.extraction_fields)
        
        reward_components = {}
        
        for field_name in action.extraction_fields:
            if field_name in ground_truth:
                extracted_count += 1
                reward_components[f"extracted_{field_name}"] = 0.1
        
        accuracy = extracted_count / total_fields if total_fields > 0 else 0
        total_reward = accuracy * 0.3  # Max 0.3 reward for extraction
        reward_components["extraction_accuracy"] = total_reward
        
        return total_reward, reward_components
    
    async def _handle_rule_matching(self, action: Action) -> Tuple[float, Dict[str, float]]:
        """Handle rule matching action."""
        ground_truth_rules = set(self.current_document.ground_truth.get("applicable_rules", []))
        
        if not action.rule_keywords:
            return 0.0, {}
        
        matched_rules = set()
        for keyword in action.rule_keywords:
            for rule in self.current_rules:
                if keyword.lower() in rule.description.lower() or keyword.lower() in rule.rule_id.lower():
                    matched_rules.add(rule.rule_id)
        
        # Calculate precision and recall
        if matched_rules:
            precision = len(matched_rules & ground_truth_rules) / len(matched_rules)
            recall = len(matched_rules & ground_truth_rules) / len(ground_truth_rules) if ground_truth_rules else 0
            f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        else:
            f1_score = 0.0
        
        total_reward = f1_score * 0.3  # Max 0.3 reward for rule matching
        reward_components = {
            "rule_matching_precision": precision * 0.15,
            "rule_matching_recall": recall * 0.15,
            "rule_matching_f1": f1_score * 0.3
        }
        
        return total_reward, reward_components
    
    async def _handle_decision(self, action: Action) -> Tuple[float, Dict[str, float]]:
        """Handle decision making action."""
        if not action.decision_data:
            return 0.0, {}
        
        ground_truth_decision = self.current_document.ground_truth.get("decision", "")
        ground_truth_confidence = self.current_document.ground_truth.get("confidence", 0.0)
        
        decision = action.decision_data.get("decision", "")
        confidence = action.decision_data.get("confidence", 0.0)
        justification = action.decision_data.get("justification", "")
        
        reward_components = {}
        
        # Decision correctness (0.2 reward)
        decision_correct = 1.0 if decision.lower() == ground_truth_decision.lower() else 0.0
        reward_components["decision_correctness"] = decision_correct * 0.2
        
        # Confidence accuracy (0.1 reward)
        confidence_diff = abs(confidence - ground_truth_confidence)
        confidence_score = max(0, 1.0 - confidence_diff)
        reward_components["confidence_accuracy"] = confidence_score * 0.1
        
        # Justification quality (0.1 reward)
        justification_score = min(1.0, len(justification) / 100)  # Simple length-based scoring
        reward_components["justification_quality"] = justification_score * 0.1
        
        total_reward = sum(reward_components.values())
        
        return total_reward, reward_components
    
    async def _handle_query(self, action: Action) -> Tuple[float, Dict[str, float]]:
        """Handle query action."""
        if not action.query:
            return 0.0, {}
        
        # Simple reward for valid queries
        query_length = len(action.query.split())
        reward = min(0.05, query_length * 0.01)  # Small reward for meaningful queries
        
        return reward, {"query_reward": reward}
    
    async def _update_observation(self, action: Action) -> Observation:
        """Update observation based on action taken."""
        obs = self._state.observation
        obs.step = self.current_step
        obs.error_message = None
        
        # Update memory with action
        obs.memory[f"action_{self.current_step}"] = action.dict()
        
        # Update specific fields based on action type
        if action.action_type == ActionType.EXTRACT and action.extraction_fields:
            # Add extracted fields to observation
            for field_name in action.extraction_fields:
                if field_name not in [f.field_name for f in obs.extracted_fields]:
                    # Simulate extraction (in real implementation, this would use NLP)
                    ground_truth = self.current_document.ground_truth.get("extracted_fields", {})
                    if field_name in ground_truth:
                        obs.extracted_fields.append(ExtractedField(
                            field_name=field_name,
                            value=ground_truth[field_name],
                            confidence=0.9,
                            source_text=f"Extracted from {self.current_document.document_id}"
                        ))
        
        elif action.action_type == ActionType.MATCH_RULES and action.rule_keywords:
            # Add matched rules to observation
            for keyword in action.rule_keywords:
                for rule in self.current_rules:
                    if keyword.lower() in rule.description.lower():
                        if rule.rule_id not in [r.rule_id for r in obs.matched_rules]:
                            obs.matched_rules.append(MatchedRule(
                                rule_id=rule.rule_id,
                                rule_text=rule.description,
                                relevance_score=0.8,
                                matched_clauses=[keyword]
                            ))
        
        elif action.action_type == ActionType.MAKE_DECISION and action.decision_data:
            # Add decision to observation
            obs.current_decision = Decision(
                decision=action.decision_data.get("decision", ""),
                confidence=action.decision_data.get("confidence", 0.0),
                justification=action.decision_data.get("justification", ""),
                applied_rules=action.decision_data.get("applied_rules", [])
            )
        
        return obs
    
    async def _check_episode_completion(self, action: Action) -> bool:
        """Check if the episode should end."""
        # Episode ends if max steps reached
        if self.current_step >= self.max_steps:
            return True
        
        # Episode ends if decision made (for medium/hard tasks)
        if self.task_difficulty in ["medium", "hard"] and action.action_type == ActionType.MAKE_DECISION:
            return True
        
        # Episode ends if extraction complete (for easy task)
        if (self.task_difficulty == "easy" and 
            action.action_type == ActionType.EXTRACT and 
            len(self._state.observation.extracted_fields) >= 3):
            return True
        
        return False
    
    async def _calculate_final_score(self) -> float:
        """Calculate final episode score."""
        ground_truth = self.current_document.ground_truth
        
        if self.task_difficulty == "easy":
            # Score based on extraction accuracy
            gt_fields = set(ground_truth.get("extracted_fields", {}).keys())
            extracted_fields = set(f.field_name for f in self._state.observation.extracted_fields)
            
            if gt_fields:
                accuracy = len(gt_fields & extracted_fields) / len(gt_fields)
            else:
                accuracy = 0.0
            
            return accuracy
        
        elif self.task_difficulty == "medium":
            # Score based on rule matching
            gt_rules = set(ground_truth.get("applicable_rules", []))
            matched_rules = set(r.rule_id for r in self._state.observation.matched_rules)
            
            if gt_rules:
                precision = len(gt_rules & matched_rules) / len(matched_rules) if matched_rules else 0
                recall = len(gt_rules & matched_rules) / len(gt_rules)
                f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            else:
                f1_score = 0.0
            
            return f1_score
        
        else:  # hard
            # Score based on decision accuracy
            if self._state.observation.current_decision:
                gt_decision = ground_truth.get("decision", "")
                gt_confidence = ground_truth.get("confidence", 0.0)
                
                decision_correct = 1.0 if self._state.observation.current_decision.decision.lower() == gt_decision.lower() else 0.0
                confidence_diff = abs(self._state.observation.current_decision.confidence - gt_confidence)
                confidence_score = max(0, 1.0 - confidence_diff)
                
                return (decision_correct * 0.7 + confidence_score * 0.3)
            else:
                return 0.0
    
    async def state(self) -> EnvironmentState:
        """Get current environment state."""
        if self._state is None:
            raise RuntimeError("Environment not initialized. Call reset() first.")
        return self._state
    
    async def evaluate_episode(self) -> EvaluationResult:
        """Evaluate the completed episode."""
        if self._state is None or not self._state.episode_complete:
            raise RuntimeError("Episode not complete. Cannot evaluate.")
        
        final_score = self._state.final_score or 0.0
        
        # Calculate component scores
        correctness = final_score  # Simplified for this implementation
        completeness = min(1.0, self.current_step / self.max_steps)
        reasoning_quality = 0.8  # Simplified - would be more complex in real implementation
        
        # Generate feedback
        if final_score >= 0.8:
            feedback = "Excellent performance! Task completed successfully with high accuracy."
        elif final_score >= 0.6:
            feedback = "Good performance. Task completed with reasonable accuracy."
        elif final_score >= 0.4:
            feedback = "Acceptable performance. Some improvements needed."
        else:
            feedback = "Poor performance. Significant improvements required."
        
        return EvaluationResult(
            task_id=f"{self.current_document.document_id}_{self.task_difficulty}",
            score=final_score,
            correctness=correctness,
            completeness=completeness,
            reasoning_quality=reasoning_quality,
            feedback=feedback,
            passed=final_score >= 0.6
        )
