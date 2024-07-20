from config import configure_setup
from classNode import JobKnowledgeGraph
from cypher_utils import make_cypher_query
from process_data import get_job_desc
from datetime import date





if __name__ == "__main__":
    
    knowledge_graph, client = configure_setup()

    # Example job description
    # with open("jd_example.txt", "r") as file:
    #     job_description = file.read()
    #

    # knowledge_graph.refresh_schema()
    # print(knowledge_graph.schema)

    with open("Knowledge_Graph/cypher/count_nodes.cypher", "r") as file:
        count_nodes_cypher = file.read()

    with open("Knowledge_Graph/cypher/count_relationships.cypher", "r") as file:
        count_relations_cypher = file.read()


    # with open("cypher/delete_all.cypher", "r") as file:
    #     delete_cypher = file.read()

    # knowledge_graph.query(delete_cypher)

    # filename = f"job_posts_data/job_posts_artificial_intelligence_{str(date.today())}.json"
    filename = f"./data/data_2024_06_23.json"

    n_processed = 0
    job_desc = get_job_desc(filename)
    for jd_info in job_desc:
        try:
            job_title, company_name, job_desc = jd_info
            job_desc = job_desc.replace('"', "'")

            system_prompt = f"""
            Help me understand the following by describing it as a detailed knowledge graph.
            Only extract and present only the factual information.
            Always return results in capitalized form
            
            Job descriptions: {job_desc}
            """

            resp = client.chat.completions.create(
            messages=[
                    {
                        "role": "user",
                        "content": system_prompt
                    }
                ],
                response_model= JobKnowledgeGraph,
            )

            cypher = make_cypher_query(resp, job_title, company_name)
            knowledge_graph.query(cypher)
            print(f"Added {job_title} @ {company_name} to Knowledge Graph.")
 
            n_processed += 1
        except Exception as e:
            print(e)
            continue


    print(f"Processed {n_processed} job postings!")

    num_node = knowledge_graph.query(count_nodes_cypher)
    num_relation = knowledge_graph.query(count_relations_cypher)

    print(num_node[0], num_relation[0])
