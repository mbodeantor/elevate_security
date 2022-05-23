import requests
import psycopg2
from flask import Flask, request, make_response
import pandas as pd
import json
import boto3

app = Flask(__name__)

def main():
    r = requests.get("https://elevateinterviews:ElevateSecurityInterviews2021@incident-api.use1stag.elevatesecurity.io/identities/")
    employee_ids = r.json()
    ip_fields = {"denial": "source_ip", "intrusion": "source_ip", "executable": "machine_ip", "probing": "ip", "other": "identifier"}

    results = {}
    event_types = ["denial", "intrusion", "executable", "misuse", "unauthorized", "probing", "other"]
    for event_type in event_types:
        r = requests.get(f"https://elevateinterviews:ElevateSecurityInterviews2021@incident-api.use1stag.elevatesecurity.io/incidents/{event_type}")
        # error handling for the status code

        for res in r.json()["results"]:
            if event_type in ip_fields:
                ip_field = ip_fields[event_type]
                # some ips not in identities
                if "." in str(res[ip_field]) and str(res[ip_field]) in employee_ids:
                    employee_id = employee_ids[str(res[ip_field])]
                elif event_type == "other":
                    employee_id = res["identifier"]
                else:
                    continue
            else:
                employee_id = res["employee_id"]

            if employee_id not in employee_ids:
                results[employee_id] = {
                                        "low": {"count": 0, "incidents": []},
                                        "medium": {"count": 0, "incidents": []},
                                        "high": {"count": 0, "incidents": []},
                                        "critical": {"count": 0, "incidents": []}
                                        }

            results[employee_id][res["priority"]]["incidents"].append(res)

    for employee in results:
        incidents = results[employee]
        for priority in incidents:
            results[employee][priority]["count"] = len(results[employee][priority]["incidents"])
            results[employee][priority]["incidents"] = sorted(results[employee][priority]["incidents"], key = lambda k: k["timestamp"])

    with open("incidents.json", "w") as f:
        json.dump(results, f)


@app.route("/incidents")
def get_incidents():
    with open("incidents.json") as f:
        body_data = json.load(f)
    response_body = {"data": body_data}

    return make_response(json.dumps(response_body), 200,
        {"Content-Type": "application/json"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
