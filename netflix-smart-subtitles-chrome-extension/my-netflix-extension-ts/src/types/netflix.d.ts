/*
 * Netflix Subtitle Downloader
 * Copyright (C) 2025 Based on Subadub by Russel Simmons
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

// Netflix API Types
export interface NetflixSubtitle {
  language: string;
  languageDescription: string;
  new_track_id: string;
  isForcedNarrative?: boolean;
  isNoneTrack?: boolean;
  rawTrackType?: string;
  ttDownloadables?: {
    [key: string]: {
      urls: Array<{ url: string }>;
    };
  };
}

export interface NetflixManifest {
  result: {
    movieId: number;
    timedtexttracks: NetflixSubtitle[];
  };
}

export interface NetflixMoviesResponse {
  result: {
    movies: {
      [movieId: string]: {
        movieId: number;
        timedtexttracks: NetflixSubtitle[];
      };
    };
  };
}

export interface NetflixAlternativeResponse {
  result: {
    result: {
      movieId: number;
      timedtexttracks: NetflixSubtitle[];
    };
  };
}

// Extension Message Types
export interface ExtensionMessage {
  type: 'NETFLIX_SUBTITLES' | 'NETFLIX_SUBTITLES_REQUEST';
  action: string;
  data?: any;
  settings?: SmartSubtitlesSettings;
}

export interface SubtitleTrack {
  id: string;
  language: string;
  languageDescription: string;
  bestUrl: string;
  isClosedCaptions: boolean;
}

export interface TracksAvailableMessage extends ExtensionMessage {
  type: 'NETFLIX_SUBTITLES';
  action: 'TRACKS_AVAILABLE';
  data: {
    movieId: number;
    tracks: SubtitleTrack[];
  };
}

export interface DownloadRequestMessage extends ExtensionMessage {
  type: 'NETFLIX_SUBTITLES_REQUEST';
  action: 'DOWNLOAD_SUBTITLE';
  trackId: string;
}

export interface GetTracksMessage extends ExtensionMessage {
  type: 'NETFLIX_SUBTITLES_REQUEST';
  action: 'GET_TRACKS';
}

// Chrome Extension Types
export interface ChromeTab {
  id: number;
  url: string;
  title: string;
}

export interface ChromeMessage {
  action: 'checkNetflixPage' | 'getSubtitles' | 'downloadSubtitle' | 'processSmartSubtitles';
  trackId?: string;
  settings?: SmartSubtitlesSettings;
}

// Smart Subtitles Types
export interface SmartSubtitlesSettings {
  enabled: boolean;
  targetLanguage: string;
  nativeLanguage: string;
  vocabularyLevel: number;
}

export interface ChromeResponse {
  success: boolean;
  isNetflixEpisode?: boolean;
  title?: string;
  url?: string;
  tracks?: SubtitleTrack[];
  movieId?: number;
  message?: string;
  error?: string;
}
