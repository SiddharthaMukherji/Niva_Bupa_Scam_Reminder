# Email Reminder Cron Job

Sends an email every 8 hours with an incrementing subject like:
Reminder 1/20, Reminder 2/20 ...

## Setup

1. Clone repo
2. Update `config.py` with your email credentials
3. Run manually:
   `python send_reminder.py`

## Cron Setup

Run:

```bash
crontab -e
```

Add:

```cron
0 */8 * * * /usr/bin/python3 /full/path/email-reminder/send_reminder.py >> /tmp/reminder.log 2>&1
```

## Notes

- Uses a local file (`counter.txt`) to track count
- Stops after `MAX_REMINDERS`
- Use Gmail App Password (not your real password)

## Important (Gmail Users)

- Enable 2FA
- Generate App Password
- Use that in `config.py`
