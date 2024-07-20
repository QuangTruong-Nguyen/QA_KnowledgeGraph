import json

def get_job_desc(filename):
    with open(filename, "r", encoding="utf-8") as file:
        job_posts = json.load(file)


    for data in job_posts.values():
        job_title, company, job_desc = data["job"], data["company"], data["job_description"]
        yield job_title, company, job_desc


if __name__ == "__main__":
    filename = "./data/data_2024_06_23.json"
    for d in get_job_desc(filename):
        print(d)