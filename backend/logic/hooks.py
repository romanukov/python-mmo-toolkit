from backend.ioc import depends
from backend.common.network.session.hooks import IConnectionHooks
from backend.common.network.session.context import context
from backend.logic.models import IdModel
from backend.logic.service import ILogicService


class LogicHooks(IConnectionHooks):
    service: ILogicService = depends(ILogicService)

    def on_server_start(self):
        print('on_server_start')

    def on_server_exit(self):
        print('on_server_exit')

    def on_connect(self):
        print('on_connect', id(context.session))

    def on_authorize(self):
        self.service.mark_player_as_online()
        player = self.service.get_player_by_id(IdModel(id=context.session.player_id))
        print('authorized', id(context.session), player['name'])

    def on_method_call(self):
        if context.session.player_id:
            player = self.service.get_player_by_id(IdModel(id=context.session.player_id))

    def on_disconnect(self):
        player = self.service.get_player_by_id(IdModel(id=context.session.player_id))
        print('on_disconnect', id(context.session), player['name'])
        self.service.mark_player_as_offline()
        player = self.service.get_player_by_id(IdModel(id=context.session.player_id))
