from pydantic import BaseModel, Field, Extra
from typing import Dict, Any, List, Optional, Union

class Location(BaseModel):
    name: str = Field(description= "Location name")
    location_type: str | None = Field(description= "Type of location: headquater, office, etc; not a country, city.")

class Education(BaseModel):
    name: str = Field(description= "Degree name such as: Bachelor of Science, Master of Engineer, etc.")
    fields: str | None = Field(description= "Fields of study such as: Computer Science, Math, Information Technology, etc.")
    status: str | None = Field(description= "Education status: graduate, ungraduate, etc.")

class Skill(BaseModel):
    name: str = Field(description= "Skill name")
    hypernym: str | None = Field(description= "Hypernym of skill")

class Work_Exper(BaseModel):
    name: str = Field(description= "Work Experience name")
    duration: Any = Field(description= "Years or months or level of experience")

class Work_Level(BaseModel):
    name: str = Field(description= "Work level: intern, senior, lead, CEO, etc.")

class Company(BaseModel):
    subdiaries: List[str] | None = Field(description= "Subsidiaries or teams belong to the company. It not, if will not be returned.")
    locations: List[Location] | None = Field(description= "Company headquarter or branches. It not, if will not be returned.")
    industry: List[str] | None = Field(description= "The industry in which the company is doing business")


class Job(BaseModel, strict=True):
    description: str = Field(description="Brief summary of what to do when applying for this job.")
    work_at: Location | None = Field(description= "Working location. If not, it will not be returned")
    work_mode: str | None = Field(description= "Work at company (Onsite), Part-time, etc. If not, it will not be returned")
    work_level: Work_Level | None = Field(description= "Word level such as: Intern, Fresher, Junior, etc.")
    education_requirements: List[Education] = Field(description="Education requirements")
    skill_requirements: List[Skill] = Field(description= "Identify and list all the technology skills mentioned. These skills can be specific tools, frameworks, programming languages, or broader categories like 'cloud computing' or 'data science'.")
    work_exper_requirements: List[Work_Exper] = Field(description="Identify the specific years or months of experience required for each position or level of experience (e.g., entry-level, mid-level, senior). If the posting mentions preferred or desired experience, include that information as well.")
    benefit_compensation: str | None = Field(description= "Benefits and compensations include: salary, dayoff, holiday, etc.")
    from_company: Company = Field(description= "The company is recruiting for this job position")


class JobKnowledgeGraph(BaseModel):
    job: Job = Field(description= "Knowledge graph about job.")