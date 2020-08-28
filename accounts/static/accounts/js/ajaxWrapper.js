/* 
MIT License

Copyright (c) 2020 daniel muremwa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Visit: https://github.com/muremwa/read-urls-extension.git

*/

const ajax = (() => {
    const requestType = {
        POST: 'POST',
        GET: 'GET'
    };
    const crossSiteHeader = {
        name: 'Access-Control-Allow-Origin',
        value: '*'
    };
    const flat200 = (status) => {
        return parseInt(status.toString().replace(/\B\d/g, '0'));
    };
    const xhr = new XMLHttpRequest();
    const addHeaders = (headers, cross) => {
        cross ? headers.push(crossSiteHeader) : void 0;
        headers.forEach((header) => {
            xhr.setRequestHeader(header.name, header.value);
        });
    };
    function __superRequest__(options) {
        // cookies?
        options.sendCookies === true ? xhr.withCredentials = true : void 0;
        // add headers if any
        options.headers && options.headers.length > 0 ? addHeaders(options.headers, options.crosssite) : void 0;
        // set response type
        xhr.responseType = options.responseType;
        // error handler
        xhr.onerror = options.error;
        // request complete
        xhr.onload = (event) => {
            if (flat200(xhr.status) === 200) {
                options.success({
                    status: xhr.status,
                    statusText: xhr.statusText,
                    response: xhr.response
                });
            }
            else {
                options.error(event);
            }
            ;
        };
    }
    ;
    /*
        send a get request
    */
    function _get_request_(options) {
        // add search params if any
        if (options.params) {
            if (typeof options.url === 'string') {
                options.url = new URL(options.url);
            }
            ;
            if (!('searchParams' in options.url)) {
                throw TypeError('The url passed is incorrect');
            }
            ;
            options.params.forEach((param) => {
                options.url.searchParams.set(param.name, param.value);
            });
        }
        ;
        xhr.open(requestType.GET, options.url);
        // download progress
        if (options.downloadprogress) {
            xhr.onprogress = (event) => {
                if (event.lengthComputable) {
                    options.downloadprogress(event.lengthComputable, event.loaded, event.total);
                }
                else {
                    options.downloadprogress(event.lengthComputable, event.loaded);
                }
                ;
            };
        }
        ;
        // call generic options
        __superRequest__(options);
        // send request bro
        xhr.send();
    }
    ;
    /*
        send A post request
    */
    function _post_request_(options) {
        if (options.data && options.form) {
            throw new Error('Both data and form are currently not supported');
        }
        ;
        // open the request
        xhr.open(requestType.POST, options.url);
        // data to be sent to back end?
        let _data = '';
        if (options.data) {
            const jsonHeader = {
                name: 'Content-type',
                value: 'application/json; charset=utf-8'
            };
            options.headers ? options.headers.push(jsonHeader) : options.headers = [jsonHeader,];
            _data = JSON.stringify(options.data);
        }
        else if (options.form) {
            _data = new FormData(options.form);
        }
        ;
        // call generic options
        __superRequest__(options);
        // upload progress start?
        options.uploadstart ? xhr.upload.onloadstart = options.uploadstart : void 0;
        // upload done?
        options.uploadend ? xhr.upload.onload = options.uploadend : void 0;
        // upload progress error?
        options.uploaderror ? xhr.upload.onerror = options.uploaderror : void 0;
        // upload progress?
        options.uploadprogress ? xhr.upload.onprogress = (event) => {
            options.uploadprogress(event.loaded, event.total);
        } : void 0;
        // send request
        xhr.send(_data);
    }
    ;
    return {
        get: (options) => _get_request_(options),
        post: (options) => _post_request_(options),
    };
})();