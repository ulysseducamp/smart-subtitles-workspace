import {
    AsbPlayerToTabCommand,
    AsbPlayerToVideoCommandV2,
    Command,
    ExtensionToVideoCommand,
    LoadSubtitlesMessage,
    Message,
    ToggleVideoSelectMessage,
} from '@project/common';
import TabRegistry from '../../services/tab-registry';

export default class LoadSubtitlesHandler {
    private readonly _tabRegistry: TabRegistry;

    constructor(tabRegistry: TabRegistry) {
        this._tabRegistry = tabRegistry;
    }

    get sender() {
        return 'asbplayerv2';
    }

    get command() {
        return 'load-subtitles';
    }

    handle(command: Command<Message>, sender: Browser.runtime.MessageSender) {
        const loadSubtitlesCommand = command as AsbPlayerToTabCommand<LoadSubtitlesMessage>;
        const toggleVideoSelectCommand: ExtensionToVideoCommand<ToggleVideoSelectMessage> = {
            sender: 'asbplayer-extension-to-video',
            // Target specific video element by 'src' if the command specifies a 'src'
            src:
                'src' in command
                    ? ((command as AsbPlayerToVideoCommandV2<LoadSubtitlesMessage>).src as string)
                    : undefined,
            message: {
                command: 'toggle-video-select',
                fromAsbplayerId: loadSubtitlesCommand.message.fromAsbplayerId,
            },
        };
        let published = false;
        this._tabRegistry
            .publishCommandToVideoElementTabs((tab) => {
                if (tab.id === loadSubtitlesCommand.tabId) {
                    published = true;
                    return toggleVideoSelectCommand;
                }

                return undefined;
            })
            .then(() => {
                if (published) {
                    browser.tabs.update(loadSubtitlesCommand.tabId, { active: true });
                }
            });

        return false;
    }
}
