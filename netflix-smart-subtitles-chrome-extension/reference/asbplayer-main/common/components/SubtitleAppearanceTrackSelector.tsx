import React from 'react';
import MenuItem from '@mui/material/MenuItem';
import TextField from '@mui/material/TextField';
import { useTranslation } from 'react-i18next';

const maxTracks = 3;

interface Props {
    track: Track;
    onTrackSelected: (track: Track) => void;
}

type Track = number | 'all';

export default function SubtitleAppearanceTrackSelector({ track, onTrackSelected }: Props) {
    const { t } = useTranslation();

    return (
        <>
            <TextField
                select
                fullWidth
                color="primary"
                variant="outlined"
                size="small"
                label={t('settings.subtitleTrack')!}
                helperText={track === 'all' ? t('settings.subtitleTrackSelectorHelper') : undefined}
                value={track}
                onChange={(e) =>
                    e.target.value === 'all' ? onTrackSelected('all') : onTrackSelected(Number(e.target.value) as Track)
                }
            >
                <MenuItem value={'all'}>{t('settings.allSubtitleTracks')}</MenuItem>
                {[...Array(maxTracks).keys()].map((i) => {
                    return (
                        <MenuItem key={i} value={i}>
                            {t('settings.subtitleTrackChoice', { trackNumber: i + 1 })}
                        </MenuItem>
                    );
                })}
            </TextField>
        </>
    );
}
