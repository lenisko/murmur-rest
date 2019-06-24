"""
api.py
All API route endpoints

:copyright: (C) 2014 by github.com/alfg.
:license:   MIT, see README for more details.
"""

from builtins import map
from builtins import str
from datetime import timedelta

from flask import request, jsonify, json, Response
from flask_classful import FlaskView

from app import app, meta
from app.utils import obj_to_dict, get_server_conf, get_server_port


class ServersView(FlaskView):
    """
    Primary interface for creating, reading and writing to mumble servers.
    """

    def index(self):
        """
        Lists all servers
        """

        servers = []
        for s in meta.getAllServers():
            servers.append({
                'id': s.id(),
                'name': get_server_conf(meta, s, 'registername'),
                'address': '%s:%s' % (
                    get_server_conf(meta, s, 'host'),
                    get_server_port(meta, s),
                ),
                'host': get_server_conf(meta, s, 'host'),
                'port': get_server_port(meta, s),
                'running': s.isRunning(),
                'users': (s.isRunning() and len(s.getUsers())) or 0,
                'maxusers': get_server_conf(meta, s, 'users') or 0,
                'channels': (s.isRunning() and len(s.getChannels())) or 0,
                'uptime_seconds': s.getUptime() if s.isRunning() else 0,
                'uptime': str(
                    timedelta(seconds=s.getUptime()) if s.isRunning() else ''
                ),
                'log_length': s.getLogLen(),
                'users': [s.getUsers()[uid].name for uid in s.getUsers().keys()] if s.isRunning() else None,
            })

        return Response(json.dumps(servers, sort_keys=True, indent=4), mimetype='application/json')

    def get(self, id):
        """
        Lists server details
        """

        id = int(id)
        s = meta.getServer(id)

        # Return 404 if not found
        if s is None:
            return jsonify(message="Not Found"), 404

        tree = obj_to_dict(s.getTree()) if s.isRunning() else None

        json_data = {
            'id': s.id(),
            'host': get_server_conf(meta, s, 'host'),
            'port': get_server_port(meta, s),
            'address': '%s:%s' % (
                get_server_conf(meta, s, 'host'),
                get_server_port(meta, s),
            ),
            'welcometext': get_server_conf(meta, s, 'welcometext'),
            'user_count': (s.isRunning() and len(s.getUsers())) or 0,
            'maxusers': get_server_conf(meta, s, 'users') or 0,
            'running': s.isRunning(),
            'uptime': s.getUptime() if s.isRunning() else 0,
            'humanize_uptime': str(
                timedelta(seconds=s.getUptime()) if s.isRunning() else ''
            ),
            'users': [s.getUsers()[uid].name for uid in s.getUsers().keys()] if s.isRunning() else None,
        }

        return jsonify(json_data)

ServersView.register(app)

if __name__ == '__main__':
    app.run(debug=True)
