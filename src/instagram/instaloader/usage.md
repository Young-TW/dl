# 程式碼說明

1. **`download_instagram_content` 函式**：
   - 合併了下載即時動態、精選即時動態、貼文和 Reels 的功能。
   - 針對每一個操作（下載即時動態、精選即時動態、貼文、Reels），根據命令列參數的不同進行操作。

2. **命令列參數**：
   - `--stories`：下載使用者的即時動態。
   - `--highlights`：下載使用者的精選即時動態。
   - `--posts`：下載使用者的貼文（圖片和非 Reels 的影片）。
   - `--reels`：下載使用者的 Reels（短影片）。
   - `--all`：下載所有內容（即時動態、精選即時動態、貼文和 Reels）。

3. **下載邏輯**：
   - 貼文和 Reels 是根據貼文的類型來區分的，`GraphVideo` 類型且 `is_video` 為 `True` 的貼文被認為是 Reels。
   - 下載的內容會分別儲存在 `target_username_posts` 和 `target_username_reels` 資料夾中。
