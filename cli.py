"""
CLI script that uses the IndeedFeed class to search for jobs by client name or reference number
"""

import sys
import pprint
from indeed import IndeedFeed


def write_csv(client, job_list):
    """_summary_

    Args:
        client_name (_type_): _description_
        jobs (_type_): _description_
    """
    client = client.replace(" ", "_")
    # write the jobs as a csv file with each job as a row
    with open(f"{client}_jobs.csv", "w", encoding=str) as f:
        headers = job_list[0].keys()
        f.write(",".join(headers) + "\n")
        for j in job_list:
            for v in j.values():
                # remove any commas in the values ottherwise
                v = v.replace(",", "")
                f.write(f"{v},")
            # add a new line after each job to create a new row
            f.write("\n")


if __name__ == "__main__":
    Indeed = IndeedFeed()

    # ask_write()

    try:
        # get the option they want to search by
        option = sys.argv[1]
        if option.lower() == "client":
            jobs = []
            try:
                client_name = input("Enter client name: ").lower()
                # Fuzzy search
                search_type = input("Do you want to do a fuzzy search? (y/n): ").lower()
                # Client type allows us to search by indivudal client or source
                client_type = input(
                    "Do you want to search by source name? (y/n): "
                ).lower()
                if search_type == "y" and client_type == "y":
                    jobs = Indeed.find_client_or_source_jobs(client_name, True, True)
                elif search_type == "y" and client_type == "n":
                    jobs = Indeed.find_client_or_source_jobs(client_name, True)
                elif search_type == "n" and client_type == "y":
                    jobs = Indeed.find_client_or_source_jobs(client_name, False, True)
                else:
                    jobs = Indeed.find_client_or_source_jobs(client_name)

                pprint.pprint(jobs, sort_dicts=False)

                write = input(
                    "Do you want to save the results to a file? (y/n): "
                ).lower()
                if write == "y":
                    write_csv(client_name, jobs)

                else:
                    print("Exiting...")
                    sys.exit(1)

            except IndexError:
                print("Please provide a client name")
        elif option.lower() == "ref":
            try:
                reference = input("Enter reference number: ").lower()
                job = Indeed.find_job_by_reference(reference)
                pprint.pprint(job, sort_dicts=False)
            except IndexError:
                print("Please provide a reference number")

    except IndexError:
        print(Indeed.feed_stats())
        sys.exit(1)
