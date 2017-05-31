from dcengine import Engine, consumer, rpc, Msg, RequestError


class DemoEngine(Engine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.request.data.get('raise_class_exc', None):
            raise RequestError('DemoEngine.__init__ : RequestError', data={'some': 'error data'})

    @rpc
    def auto_rpc(self):
        """
        Simply send result back, exception is automatically processed.
        Use RequestError for sending error data
        """
        print('called: DemoEngine.auto_rpc received data: {}'.format(self.request.data))

        if self.request.data.get('raise_exc', None):
            raise RequestError('DemoEngine.auto_rpc : RequestError', data={'some': 'error data'})

        return {'some': 'answer'}

    @rpc(send=False)
    def manual_rpc(self):
        """
        In this case, you must manually send message and handle exceptions.
        """
        print('called: DemoEngine.manual_rpc received data: {}'.format(self.request.data))

        e = None

        if self.request.data.get('raise_exc', None):
            e = Exception('DemoEngine.manual_rpc : Exception')
            msg = Msg(
                error=e.__repr__(),
                error_data={'some': 'error data'},
                cmd_id=self.request.cmd_id,
                status='error'
            )
        else:
            msg = Msg(
                data={'some': 'data'},
                cmd_id=self.request.cmd_id
            )
        self.send(msg)
        if e:
            raise e

    @consumer
    def auto_consumer(self):
        """
        Simply send result to callbacks if it specified, exception is automatically processed.
        If you want send error data use RequestError.
        """
        print('called: DemoEngine.auto_consumer, received data: {}'.format(self.request.data))

        if self.request.data.get('raise_exc', None):
            if self.request.data.get('exc_type', None) == 'RequestError':
                raise RequestError('DemoEngine.auto_consumer : RequestError', {'some': 'error data'})
            else:
                raise Exception('DemoEngine.auto_consumer : Raw Exception')

        if self.request.data['return_result']:
            return {'some': 'data'}

    @consumer(send=False)
    def manual_consumer(self):
        """
        In this case, you must manually send message and handle exceptions.
        """
        print('called: DemoEngine.manual_consumer received data: {}'.format(self.request.data))

        if self.request.data.get('raise_exc', None):
            e = Exception('DemoEngine.manual_consumer : Exception')
            msg = Msg(
                error=e.__repr__(),
                error_data={'some': 'error data'},
                consumers=self.request.callbacks,
                status='error'
            )
            self.send(msg)
            raise e
        else:
            msg = Msg(
                data={'some': 'data'},
                consumers=self.request.callbacks
            )
            self.send(msg)

#
# class DemoEngine1(Engine):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#     @rpc
#     def auto_rpc(self):
#         """
#         Simply send result back, exception is automatically processed.
#         """
#         print('called: {}.{} received data: {}'.format(self.__class__.__name__, 'auto_rpc', self.request.data))
#
#         if self.request.data.get('raise_exc', None):
#             raise Exception('{}.{} : {}'.format(self.__class__.__name__, 'auto_rpc', 'raise_exc'))
#
#         return {'received': self.request.data}
