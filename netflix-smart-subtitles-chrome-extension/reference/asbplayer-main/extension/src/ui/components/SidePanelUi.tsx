import { useEffect, useMemo, useState } from 'react';
import SidePanel from './SidePanel';
import { createTheme } from '@project/common/theme';
import { AsbplayerSettings, SettingsProvider } from '@project/common/settings';
import { ExtensionSettingsStorage } from '../../services/extension-settings-storage';
import { ExtensionMessage, useChromeExtension } from '@project/common/app';
import ThemeProvider from '@mui/material/styles/ThemeProvider';
import CssBaseline from '@mui/material/CssBaseline';
import Paper from '@mui/material/Paper';
import { StyledEngineProvider } from '@mui/material/styles';

const settingsProvider = new SettingsProvider(new ExtensionSettingsStorage());

const SidePanelUi = () => {
    const [settings, setSettings] = useState<AsbplayerSettings>();
    const extension = useChromeExtension({ component: 'sidePanel' });
    const theme = useMemo(() => settings && createTheme(settings.themeType), [settings]);

    useEffect(() => {
        settingsProvider.getAll().then(setSettings);
    }, []);

    useEffect(() => {
        return extension.subscribe((message: ExtensionMessage) => {
            if (message.data.command === 'settings-updated') {
                settingsProvider.getAll().then(setSettings);
            }
        });
    }, [extension]);

    if (!settings || theme === undefined) {
        return null;
    }

    return (
        <StyledEngineProvider injectFirst>
            <ThemeProvider theme={theme}>
                <CssBaseline />
                <Paper square style={{ width: '100%', height: '100%' }}>
                    <SidePanel settings={settings} extension={extension} />
                </Paper>
            </ThemeProvider>
        </StyledEngineProvider>
    );
};

export default SidePanelUi;
