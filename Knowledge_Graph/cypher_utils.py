def add_job_nodes(response, job_name):
    job = response.job

    # Create job nodes
    cypher = f'''
    CREATE (job:Job {{name: "{job_name}"}})
    '''

    # Job description
    if job.description:
        cypher += f'SET job.description = "{job.description}"'

    # Work mode
    if job.work_mode:
        cypher += f'''
        SET job.work_mode = "{job.work_mode}"
        '''

    # Benefits & Compensations
    if job.benefit_compensation:
        cypher += f'''
        SET job.benefit_compensation = "{job.benefit_compensation}"
        '''

    # Locations
    if job.work_at:
        cypher += f'''
    MERGE (loc: Location {{name: "{job.work_at.name}", location_type: "{job.work_at.location_type}"}})
    MERGE (job)-[:WORK_AT]->(loc)
    '''

    # Work Levels
    if job.work_level:
        cypher += f'''
    MERGE (level: Work_LV {{name: "{job.work_level.name}"}})
    MERGE (job)-[:AT_LEVEL]->(level)
    '''

    # Required educations
    if job.education_requirements:
        for i, edu in enumerate(job.education_requirements):
            cypher += f'''
        CREATE (edu_{i}:Education {{name: "{edu.name}"}})
        MERGE (job)-[:REQUIRES]->(edu_{i})
            '''

            if edu.fields:
                cypher += f'SET edu_{i}.fields = "{edu.fields}"'

            if edu.status:
                cypher += f'SET edu_{i}.status = "{edu.status}"'

    # Required skills
    if job.skill_requirements:
        for i, skill in enumerate(job.skill_requirements):
            cypher += f'''
        MERGE (skill_{i}:Skill {{name: "{skill.name}"}})
        MERGE (job)-[:REQUIRES]->(skill_{i})
            '''

            if skill.hypernym:
                cypher += f'''
        MERGE (hypernym_{i}:Skill {{name: "{skill.hypernym}"}})
        MERGE (skill_{i})-[:HYPERNYM]->(hypernym_{i})  
        '''

    # Required work experiences
    if job.work_exper_requirements:
        for i, exper in enumerate(job.work_exper_requirements):
            cypher += f'''
        MERGE (exper_{i}:Work_Exper {{name: "{exper.name}"}})
        MERGE (job)-[:REQUIRES]->(exper_{i})
        '''

            if exper.duration:
                cypher += f'SET exper_{i}.duration = "{exper.duration}"'

    return cypher

def add_company_nodes(response, company_name):
    company = response.job.from_company

    cypher = f'''
    MERGE (company:Company {{name: "{company_name}"}})
    MERGE (job)-[:FROM]->(company)
    MERGE (company)-[:RECRUITES]->(job)
        '''

    if company:
        if company.subdiaries:
            for i, sub in enumerate(company.subdiaries):
                cypher += f'''
            MERGE (sub_{i}:Company {{name: "{sub}"}})
            MERGE (company)-[:SUBDIARY]->(sub_{i})
                '''

        if company.locations:
            for i, loc in enumerate(company.locations):
                cypher += f'''
            MERGE (loc_{i}:Location {{name: "{loc.name}"}})
            MERGE (company)-[:LOCATES_IN]->(loc_{i})
                '''

                if loc.location_type:
                    cypher += f'SET loc_{i}.location_type = "{loc.location_type}"'

        if company.industry:
            for i, industry in enumerate(company.industry):
                cypher += f'''
            MERGE (industry_{i}:Industry {{name: "{industry}"}})
            MERGE (company)-[:OPERATES_IN]->(industry_{i})
                '''

    return cypher


def make_cypher_query(response, job_title, company_name):
    job_cypher = add_job_nodes(response, job_title)
    company_cypher = add_company_nodes(response, company_name)
    return job_cypher + company_cypher