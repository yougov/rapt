import json

# example
# ex = {"time": "2014-10-08T15:42:33.032207",
#       "message": "eric.larson swarmed pangaea-3.3.7-prod-worker\n\n        App: pangaea\n        Version: 3.3.7\n        Config Name: prod\n        Proc Name: worker\n        Squad: ldc\n        Memory: \n        Size: 5\n        Balancer: None\n        Pool: None\n",
#       "tags": ["user", "swarm"],
#       "title": "eric.larson: swarm pangaea-3.3.7-prod-worker"}
# {"time": "2014-10-08T15:43:07.689344", "message": "Uptests passed for swarm pangaea-3.3.7-prod-e7977e6f-worker", "tags": ["success", "uptest"], "title": "Uptests passed"}


class SwarmEventProps(object):

    @property
    def deploy_title(self):
        if not hasattr(self, '_deploy_title'):
            self._deploy_title = '%s-%s-%s' % (self.swarm.app_name,
                                               self.swarm.version,
                                               self.swarm.proc_name)
        return self._deploy_title

    @property
    def build_title(self):
        if not hasattr(self, '_build_title'):
            self._build_title = '%s-%s' % (self.swarm.app_name,
                                           self.swarm.version)
        return self._build_title


class SwarmEvents(SwarmEventProps):
    format_tmpl = '{time} {title} {tags}'

    def __init__(self, swarm, vr):
        self.swarm = swarm
        self.vr = vr
        self.username = self.vr.username
        self.deployed = 0
        self.destroyed = 0
        self.routed = False

    def user_swarm_event(self, event):
        if 'user' in event['tags'] and 'swarm' in event['tags']:
            if self.username in event['title']:
                return event

    def swarm_build_event(self, event):
        if 'build' in event['tags']:
            if self.build_title in event['title']:
                return event

    def swarm_deploy_event(self, event):
        if 'deploy' in event['tags']:
            if self.deploy_title in event['title']:
                self.deployed += 1
                return event

    def proc_event(self, event):
        if 'proc' in event['tags']:
            if 'deleted' in event['tags']:
                self.destroyed += 0
            # we can reuse the deploy title
            if self.deploy_title in event['title']:
                return event

    def route_event(self, event):
        if 'route' in event['tags'] and self.build_title in event['title']:
            self.routed = True

    def done(self):
        cleaned_up = self.destroyed == self.swarm.size
        deployed = self.deployed == self.swarm.size
        if deployed and self.routed and cleaned_up:
            return True

        return False

    def __iter__(self):
        """Find the events for a specific swarm."""
        handlers = [
            self.user_swarm_event,
            self.swarm_build_event,
            self.swarm_deploy_event,
        ]

        for event in self.vr.events():
            event = json.loads(event.data)
            for handler in handlers:
                e = handler(event)
                if e:
                    yield self.format(e)

                if self.done():
                    break

    def format(self, event):
        message = self.format_tmpl.format(**event)
        if 'failure' in event['tags']:
            message += '\n\n' + event['message']
        return message
