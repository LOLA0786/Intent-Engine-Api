from flask import Flask, request, jsonify
from policy_diff_and_dryrun import dry_run

app = Flask(__name__)

@app.route("/simulate", methods=["POST"])
def simulate():
    data = request.json
    result = dry_run(
        data["policy_version"],
        data["action"],
        data["principal"],
        data["context"]
    )
    return jsonify(result)

if __name__ == "__main__":
    app.run(port=7000)
