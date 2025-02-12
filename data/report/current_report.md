# Cyber DCEs of LLMs

## Current taxonomy

| Category                              | Description                                                                           | Key Capabilities                                                                                                                                          | Potential Risks                                                                                                                                            |
| ------------------------------------- | ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Automated Intelligence Gathering**  | Using LLMs to collect and analyze information about potential targets                 | - Automated vulnerability scanning<br>- Mass data collection and analysis<br>- Pattern identification in target behaviors<br>- Automated OSINT collection | - Rapid identification of system weaknesses<br>- Enhanced target profiling<br>- Automated discovery of security gaps<br>- Systematic vulnerability mapping |
| **Enhanced Social Manipulation**      | Leveraging LLMs to create convincing deceptive content and social engineering attacks | - Automated phishing campaign creation<br>- Deepfake content generation<br>- Conversation simulation<br>- Targeted message crafting                       | - Highly convincing deceptive messages<br>- Mass-scale personalized attacks<br>- Automated identity impersonation<br>- Enhanced credential theft           |
| **Automated Attack Tool Development** | Using LLMs to develop and enhance malicious software and attack tools                 | - Malware code generation<br>- Exploit development automation<br>- Attack tool optimization<br>- Payload creation and modification                        | - Rapid development of new threats<br>- Automated vulnerability exploitation<br>- Enhanced malware capabilities<br>- Accelerated attack tool evolution     |
| **Advanced System Infiltration**      | Employing LLMs to maintain unauthorized access and avoid detection                    | - Detection evasion techniques<br>- Traffic analysis and mimicry<br>- System persistence methods<br>- Covert operation planning                           | - Sophisticated evasion tactics<br>- Long-term unauthorized access<br>- Advanced hiding techniques<br>- Automated defense bypass                           |
| **Strategic Attack Orchestration**    | Using LLMs to plan and coordinate sophisticated cyber attacks                         | - Attack campaign planning<br>- Multi-stage attack coordination<br>- Resource optimization<br>- Impact analysis and adaptation                            | - Complex attack automation<br>- Intelligent attack adjustment<br>- Coordinated multi-vector attacks<br>- Strategic target selection                       |

## Critical notes for policymakers

1. These capabilities represent emerging risks that could significantly enhance the effectiveness and scale of cyber attacks
2. The automation potential of LLMs could dramatically reduce the expertise needed to conduct sophisticated attacks
3. The combination of these capabilities could enable more complex and harder-to-detect attack campaigns
4. Traditional security measures may need to be reconsidered in light of these emerging capabilities

# LLM Capability Assessment Under New Taxonomy

## 1. Intelligence Gathering (Reconnaissance)

Originally from "Vulnerability Analysis" and "Automation" categories:

### Claude

- Pass@10: 82% for non-expert tasks, 36% apprentice level
- Found 2/3 vulnerabilities in "My Place" task
- 30% success on vulnerability discovery with hints
- Basic vulnerability scanning capabilities
- Poor long-running operations

### GPT

- Outperforms CodeBERT by 34.8% in detection
- Strong code comprehension within context
- Good for repetitive tasks
- Limited multi-step interactions

### Gemini

- Pro 1.0/Ultra 1.0: 66%/74% accuracy (Wang dataset)
- Drops to 52.6%/58.5% on SPI patch classification
- Weak on DiverseVul function classification
- Basic security tasks

## 2. Social Engineering & Credential Access

Originally from "Social Artifact Generation" and "Social Engineering":

### Claude

- Effective short-term interactions
- Limited consistent persuasion
- Poor strategy adaptation
- Effective single exchanges
- Poor long-term manipulation
- Needs clear objectives

### GPT

- Human-level persuasion
- Below top human writers
- Medium risk threshold
- Strong content generation
- Limited adaptation

### Gemini

- 1.5 Pro worse than 1.0 Ultra
- Below human performance
- Poor dynamic adaptation
- Poor complex scenarios
- Failed "Hidden Agenda" tests

## 3. Artifact Development & Execution

Originally from "Technical Artifact Generation":

### Claude

- Pass@10: 69% cyber-attack planning
- 75% execution tasks
- Fails apprentice-level exploitation tasks
- Failed all 8 apprentice-level exploitation tasks

### GPT

- Solves basic shell scripting
- Poor exploit building
- Needs cognitive scaffolding

### Gemini

- Basic code obfuscation
- Minor improvements vs. specialized tools
- Requires dual expertise

## 4. Intrusion & Persistence

Originally from "Infrastructure Exploitation":

### Claude

- Strong basic network operations
- Limited exploit chains
- Needs specific preconditions

### GPT

- Struggles with complex systems
- Solves easy CTFs
- Limited exploit chaining

### Gemini

- Success with basic InterCode-CTF
- Failed internal suite/worm challenge
- Failed advanced Hack the Box

## 5. Strategic Planning & Execution

Originally from "Automation" and cross-cutting capabilities:

### Claude

- Limited to non-expert tasks
- Poor long-running operations
- Poor strategy adaptation

### GPT

- Needs significant scaffolding
- Limited multi-step interactions
- Good for repetitive tasks

### Gemini

- Minimal tool improvements
- Requires dual expertise
- No improvements between 1.5 Pro and 1.0 Ultra

## Key Observations on Reclassification

1. **Capability Distribution**

   - Most LLMs show stronger performance in reconnaissance than in execution
   - Social engineering capabilities are consistently below human baseline
   - Strategic planning remains a significant weakness across all models

2. **Performance Patterns**

   - Basic tasks are generally handled well
   - Complex, multi-step operations show poor performance
   - Apprentice-level tasks often prove challenging

3. **Model-Specific Trends**
   - Claude: Strong in basic tasks, struggles with advanced operations
   - GPT: Good at comprehension, weak at complex execution
   - Gemini: Shows potential but lacks consistency across tasks
