import socket
import ssl
import certifi

import h2.connection
import h2.settings
import h2.events
from urllib.parse import urlsplit

SERVER_PORT = 443


def run(urls, verbose=False):
  """HTTP/2 downloader using h2 library."""
  first_url = urls[0]
  parsed_url = urlsplit(first_url)
  SERVER_NAME = parsed_url.hostname

  socket.setdefaulttimeout(15)
  ctx = ssl.create_default_context(cafile=certifi.where())
  ctx.set_alpn_protocols(["h2"])

  s = socket.create_connection((SERVER_NAME, SERVER_PORT))
  s = ctx.wrap_socket(s, server_hostname=SERVER_NAME)

  c = h2.connection.H2Connection()

  c.initiate_connection()
  c.update_settings({h2.settings.SettingCodes.INITIAL_WINDOW_SIZE: 1048576})  # 1 MB
  c.increment_flow_control_window(16777216)  # 16 MB

  s.sendall(c.data_to_send())

  active_streams = {}
  bodies = {}
  status_codes = {}

  for url in urls:
    stream_id = c.get_next_available_stream_id()
    parsed_url = urlsplit(url)
    PATH = parsed_url.path or "/"
    if parsed_url.query:
      PATH += f"?{parsed_url.query}"

    headers = [
        (":method", "GET"),
        (":path", PATH),
        (":authority", SERVER_NAME),
        (":scheme", "https"),
        ("user-agent", "recontradownloader/1.0"),
    ]
    c.send_headers(stream_id, headers, end_stream=True)
    bodies[stream_id] = bytearray()
    active_streams[stream_id] = url

  s.sendall(c.data_to_send())

  completed_streams = set()
  total_streams = set(active_streams.keys())

  while completed_streams != total_streams:
    data = s.recv(65536 * 1024)
    if not data:
      break

    events = c.receive_data(data)
    for event in events:
      if isinstance(event, h2.events.ResponseReceived):
        for name, value in event.headers:
          if name == b":status":
            status_codes[event.stream_id] = value.decode()
            # if verbose:
            #   print(f"Stream {event.stream_id} - Status: {value.decode()}")

      if isinstance(event, h2.events.DataReceived):
        c.acknowledge_received_data(
            event.flow_controlled_length, event.stream_id
        )
        if event.stream_id in bodies:
          bodies[event.stream_id].extend(event.data)

      if isinstance(event, h2.events.StreamEnded):
        if event.stream_id in total_streams:
          completed_streams.add(event.stream_id)

      if isinstance(event, h2.events.StreamReset):
        completed_streams.add(event.stream_id)

    outbound = c.data_to_send()
    if outbound:
      s.sendall(outbound)

  c.close_connection()
  s.sendall(c.data_to_send())
  s.close()

  # Mostrar estados si hubo algún problema
  for sid, status in status_codes.items():
    if status != "200":
      print("Error")

  results = [bytes(bodies[sid]) for sid in sorted(total_streams)]
  return results


# Prueba con la URL proporcionada
# url = "https://files.pythonhosted.org/packages/df/bf/f7da0350254c0ed7c72f3e33cef02e048281fec7ecec5f032d4aac52226b/jinja2-3.1.6.tar.gz"
# downloaded = run(urls=[url])
# print(
#     f"Received: {len(downloaded[0]) if downloaded else 0} bytes"
# )