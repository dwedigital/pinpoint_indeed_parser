# Description: Command line interface for the IndeedFeed

from indeed import IndeedFeed
import sys
import pprint


# Removing for now as have a better way to handle this in the IndeedFeed class
# def ask_write():
#     write = input("Do you want to re-create the feed file? (y/n): ")
#     if write.lower() == "y":
#         IndeedFeed().write_feed()


def pretty_print(jobs):
    for job in jobs:
        print(
            f"Company: {job['Company']}\nJob Reference: {job['Job Reference']}\nJob Title: {job['Job Title']}\n"
        )


if __name__ == "__main__":

    Indeed = IndeedFeed()
    # ask_write()

    try:
        # get the option they want to search by
        option = sys.argv[1]
        if option.lower() == "client":
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
                pretty_print(jobs)
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
