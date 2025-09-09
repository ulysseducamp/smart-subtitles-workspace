import { AsbPlayerToVideoCommand, Command, ExtensionToVideoCommand, Message } from '@project/common';

export default class AsbplayerToVideoCommandForwardingHandler {
    get sender() {
        return 'asbplayer';
    }

    get command() {
        return null;
    }

    handle(command: Command<Message>, sender: Browser.runtime.MessageSender) {
        const asbplayerToVideoCommand = command as AsbPlayerToVideoCommand<Message>;
        const extensionToVideoCommand: ExtensionToVideoCommand<Message> = {
            sender: 'asbplayer-extension-to-video',
            message: asbplayerToVideoCommand.message,
            src: asbplayerToVideoCommand.src,
        };

        browser.tabs.sendMessage(asbplayerToVideoCommand.tabId, extensionToVideoCommand);
        return false;
    }
}
