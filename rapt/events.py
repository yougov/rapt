class SwarmEventProps(object):

    @property
    def deploy_title(self):
        if not hasattr(self, '_deploy_title'):
            self._deploy_title = '%s-%s-%s' % (self.app_name,
                                               self.version,
                                               self.proc_name)
        return self._deploy_title

    @property
    def build_title(self):
        if not hasattr(self, '_build_title'):
            self._build_title = '%s-%s' % (self.app_name,
                                           self.version)
        return self._build_title


class SwarmEvents(SwarmEventProps):

    def __init__(self, app_name, version, proc_name, username):
        self.app_name = app_name
        self.version = version
        self.proc_name = proc_name
        self.username = username
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

    def __call__(self, event):
        handlers = [
            self.user_swarm_event,
            self.swarm_build_event,
            self.swarm_deploy_event,
        ]
        for handler in handlers:
            e = handler(event)
            if e:
                return e


FORMAT_TMPL = '{time} {title} {tags}'


def format_event(event):
    tail = []
    for k, v in event.items():
        if k not in ['time', 'title', 'tags', 'message']:
            tail.append('%s: %s' % (k, v))

    message = FORMAT_TMPL.format(**event)

    if tail:
        message += ' ' + ' '.join(tail)

    if 'failure' in event['tags'] or 'failed' in event['tags']:
        message += '\n\n' + event['message']
    return message


def filtered_events(vr, handlers=None):
    if not handlers:
        handlers = [lambda x: x]

    for event in vr.events():
        for handler in handlers:
            message = handler(event)
            if message:
                yield format_event(message)

            if message and 'done' in event['tags']:
                return
