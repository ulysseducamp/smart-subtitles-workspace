/*
 * Smart Netflix Subtitles
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

// React entry point for the popup
import React from 'react';
import { createRoot } from 'react-dom/client';
import { Popup } from './Popup';

// Import Tailwind CSS styles
import './styles.css';

console.log('Smart Netflix Subtitles: Popup script loaded (React)');
console.log('Smart Netflix Subtitles: WEBAPP_URL =', process.env.WEBAPP_URL);

// Mount React app
const container = document.getElementById('root');
if (container) {
  const root = createRoot(container);
  root.render(
    <React.StrictMode>
      <Popup />
    </React.StrictMode>
  );
  console.log('Smart Netflix Subtitles: React app mounted');
} else {
  console.error('Smart Netflix Subtitles: Root element not found');
}
