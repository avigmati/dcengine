import { dce, consumer } from 'dcengine-client'


function RequestException(error, error_data) {
    this.error = error;
    this.error_data = error_data;
}


@consumer
export class DemoConsumer {
    consumer(data, error, error_data) {
        if (error) {
            throw new RequestException('DemoConsumer error: ' + error, error_data);
        } else {
            console.log('DemoConsumer: ', data);
        }
    }
}


@consumer
export class DemoConsumer2 {
    consumer(data, error, error_data) {
        if (error) {
            throw new RequestException('DemoConsumer2 error: ' + error, error_data);
        } else {
            console.log('DemoConsumer2: ', data);
        }
    }
}


// CONSUMER EXAMPLE USAGE

console.log('call auto_consumer');
dce('DemoEngine.auto_consumer', {'return_result': true, 'callbacks': ['DemoConsumer']});

(async () => {
    try {
        console.log('call non exist');
        await dce('Non.exist', {'return_result': true, 'callbacks': ['DemoConsumer']});
    } catch (err) {
        console.log('Call non exist method:', err);
    }
})();

console.log('call auto_consumer with two callbacks');
dce('DemoEngine.auto_consumer', {'return_result': true, 'callbacks': ['DemoConsumer', 'DemoConsumer2']});

console.log('call auto_consumer with no callbacks. in this case result will come in DCEngine.base_consumer');
dce('DemoEngine.auto_consumer', {'return_result': true});

console.log('call auto_consumer which raises Raw exception with specified callbacks');
dce('DemoEngine.auto_consumer', {'raise_exc': true, 'callbacks': ['DemoConsumer']});

console.log('call auto_consumer which raises RequestError exception with specified callbacks');
dce('DemoEngine.auto_consumer', {'raise_exc': true, 'exc_type': 'RequestError', 'callbacks': ['DemoConsumer']});

console.log('call auto_consumer which raises exception with no callbacks. in this case error handling will be in DCEngine.base_consumer');
dce('DemoEngine.auto_consumer', {'raise_exc': true});

console.log('call manual_consumer');
dce('DemoEngine.manual_consumer', {'callbacks': ['DemoConsumer']});

console.log('call manual_consumer which raises exception');
dce('DemoEngine.manual_consumer', {'raise_exc': true});


// RPC EXAMPLE USAGE

(async () => {
    let resp = await dce('DemoEngine.auto_rpc', {'some': 'data'});
    console.log('Call auto_rpc result:', resp);

    try {
        await dce('Non.exist', {'some': 'data'});
    } catch (err) {
        console.log('Call non exist method:', err);
    }

    try {
        await dce('DemoEngine.auto_rpc', {'raise_exc': true});
    } catch (err) {
        console.log('Call auto_rpc with exception:', err.error, err.data);
    }

    try {
        await dce('DemoEngine.auto_rpc', {'raise_class_exc': true});
    } catch (err) {
        console.log('Call auto_rpc with class exception:', err.error, err.data);
    }

    let resp2 = await dce('DemoEngine.manual_rpc', {'some': 'data'});
    console.log('Call manual_rpc result:', resp2);

    try {
        await dce('DemoEngine.manual_rpc', {'raise_exc': true});
    } catch (err) {
        console.log('Call manual_rpc with exception:', err.error, err.data);
    }
})();
