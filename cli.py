# Description: Command line interface for the IndeedFeed

from indeed import IndeedFeed
import sys
import pprint


def write_csv(client_name, jobs):
    client_name = client_name.replace(" ", "_")
    # write the jobs as a csv file with each job as a row and the keys in the dictionary as columns
    with open(f"{client_name}_jobs.csv", "w") as f:
        headers = jobs[0].keys()
        f.write(",".join(headers) + "\n")
        for job in jobs:
            for k, v in job.items():
                # remove any commas in the values ottherwise they will be treated as separate columns
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
                # Fuzzy search means that the client name can be a substring of the company/source name
                search_type = input("Do you want to do a fuzzy search? (y/n): ").lower()
                # Client type allows us to search by indivudal client or source (useful if our client is a RPO/Recruiter with multiple clients)
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

                pprint.pprint(jobs, sort_dicts=False, underscore_numbers=True)

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
                pprint.pprint(job, sort_dicts=False, underscore_numbers=True)
            except IndexError:
                print("Please provide a reference number")

    except IndexError:
        print(Indeed.feed_stats())
        sys.exit(1)
