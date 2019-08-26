---
permalink: /issue/
toc: true
---

## Report Issues

If you found any issue, please send email to qiuwch@gmail.com (Weichao Qiu) or open an issue in `github.com/unrealcv/unrealcv` repo.

## Trouble Shooting

If the client failed to connect to server, please check whether the default port 9000 has been used by other programs.

- In Linux, use `sudo lsof -i -P -n | grep LISTEN`
- In Windows, use `netstat.exe -a -b` or `resmon.exe` to find out.

## Known issues

- The editor might crash when the editor is not in `play` mode
- Sometimes the server in linux will report unknown socket error, which requires restarting the server.
- Data generation speed: the project was initially designed for offline data generation and the speed is not a high priority. If you want to achieve faster speed. You can run multiple instances in the server, or by tweaking configuration to lower image quality to make it suitable for reinforcement learning.