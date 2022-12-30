import http.client

def test_get_health_endpoint():
    conn = http.client.HTTPConnection("localhost", 5000)
    conn.request("GET", "/_healthz")
    res = conn.getresponse()
    assert "HEALTHY" in res.read().decode("utf-8")

def test_get_root_endpoint():
    conn = http.client.HTTPConnection("localhost", 5000)
    conn.request("GET", "")
    res = conn.getresponse()
    assert "user_agent" in res.read().decode("utf-8")
