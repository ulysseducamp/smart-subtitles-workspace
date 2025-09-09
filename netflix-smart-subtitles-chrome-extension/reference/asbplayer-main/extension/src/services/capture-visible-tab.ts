export const captureVisibleTab = async (tabId: number): Promise<string> => {
    const tab = await browser.tabs.get(tabId);
    return await browser.tabs.captureVisibleTab(tab.windowId, { format: 'jpeg', quality: 100 });
};
