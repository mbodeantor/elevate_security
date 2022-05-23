# elevate_security

**How to run**

The script can be run from the command line to start the API once the dependent packages are installed. This will host it locally and can be reached at http://127.0.0.1:9000/incidents

**Overall Approach**

I focused on the fact that the API response time had to be under a second and that events did not have to returned any where near real time. Especially with the time constraints to develop a solution, I tried to keep it as simple as possible. With this in mind, I created a main function with the intention that it would be scheduled in a cron job to run at least every 30 minutes. This function first gets the employee ids associated with known IP addresses from the identitites endpoints. Then it cycles through each incident from each event type endpoint, looks up the employee id if the incident has an IP address associated with it, and then stores the incident by priority under the corresponding employee id in a results dictionary.

In the next step the function loops over the completed results dictionary, counts the number of events under each priority level and enters it into the dictionary, then sorts the incidents lists by timestamp. Then the results are written out to a json file locally. This makes the actual API endpoint very simple as it just reads from the results file and returns the json stored there.

**Other Approaches**

More traditional approaches I considered including storing the results in a redis cache or loading them into a postgres database. However given the time constraints and minimal requirements I favored this more simplistic approach. This is likely to be one of the first improvements that would need to be made in order to put the API into production. The last approach I considered before my final was to load the results into s3 and this would be an easy change to start the hardening process.

**Hardening the API**

In addition to modifying the approach as mentioned above, there were a few things I didn't have time for in my current approach. The most crucial would be add error handling for the requests to add retries if they fail to make sure all incidents are returned. The next would be to get the main function running in a cron job (or a more advanced job scheduler like airflow) on an accessible server in order to make the API more useful. Finally the actually API portion would also need to be hosted for the same reason.
