# Description: Command line interface for the IndeedFeed

from indeed import IndeedFeed
import sys


# Removing for now as have a better way to handle this in the IndeedFeed class
# def ask_write():
#     write = input("Do you want to re-create the feed file? (y/n): ")
#     if write.lower() == "y":
#         IndeedFeed().write_feed()


if __name__ == "__main__":

    Indeed = IndeedFeed()
    # ask_write()

    try:
        # get the option they want to search by
        option = sys.argv[1]
        if option.lower() == "client":
            try:
                client_name = input("Enter client name: ").lower()
                search_type = input("Do you want to do a fuzzy search? (y/n): ").lower()
                if search_type == "y":
                    jobs = Indeed.find_client_jobs(client_name, True)
                else:
                    jobs = Indeed.find_client_jobs(client_name)
                print(f"Total: {len(jobs)}\n\n{jobs}\n")
            except IndexError:
                print("Please provide a client name")
        elif option.lower() == "ref":
            try:
                reference = input("Enter reference number: ").lower()
                job = Indeed.find_job_by_reference(reference)
                print(job)
            except IndexError:
                print("Please provide a reference number")

    except IndexError:
        print(Indeed.feed_stats())
        sys.exit(1)
