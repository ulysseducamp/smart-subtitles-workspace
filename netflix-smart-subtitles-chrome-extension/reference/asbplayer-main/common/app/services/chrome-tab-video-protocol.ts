import { Message } from '@project/common';
import ChromeExtension, { ExtensionMessage } from './chrome-extension';
import { VideoProtocol, VideoProtocolMessage } from './video-protocol';

export default class ChromeTabVideoProtocol implements VideoProtocol {
    private readonly tabId: number;
    private readonly src: string;
    private readonly extension: ChromeExtension;
    private readonly listener: (message: ExtensionMessage) => void;
    private readonly unsubscribeFromExtension: () => void;

    onMessage?: (message: VideoProtocolMessage) => void;

    constructor(tabId: number, src: string, extension: ChromeExtension) {
        this.tabId = tabId;
        this.src = src;
        this.listener = (message) => {
            if (message.tabId === tabId && message.src === src) {
                this.onMessage?.({
                    data: message.data,
                });
            }
        };

        this.unsubscribeFromExtension = extension.subscribe(this.listener);
        this.extension = extension;
    }

    postMessage(message: Message) {
        this.extension.sendMessageToVideoElement(message, this.tabId, this.src);
    }

    close() {
        this.unsubscribeFromExtension();
    }
}
