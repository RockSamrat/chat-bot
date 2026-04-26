# Quick Reference - Conversation Storage Fixed

## The Issue
❌ Conversations not being saved to JSON file

## The Fix
✅ Changed Flask working directory to project root (3 lines of code)

## Test It
```bash
python3 test_conversation_saving.py
```

## Use It
```bash
# Start Flask server
python3 -m backend.server

# Watch for these messages:
# [server] Working directory: /home/krish-naharki/Documents/chat-bot
# [server] Conversations will be saved to: .../data/conversations/conversations.json
```

## Send a Message
Via your Tkinter GUI or use curl:
```bash
TOKEN="your-jwt-token"
curl -X POST http://localhost:5000/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question":"Hello!"}'
```

## Check the File
```bash
cat data/conversations/conversations.json
```

## Debug Messages
When you send a message, watch the Flask console for:
```
[chat] Creating new conversation for user john
[chat] Conversation saved: True
[chat] User message saved: True
[chat] Bot message saved: True
```

## Files Changed
- `backend/server.py` - Working directory fix + debug logging
- `test_conversation_saving.py` - NEW: Test script
- `TROUBLESHOOTING_GUIDE.md` - NEW: Help guide
- `FIX_SUMMARY.md` - NEW: Detailed summary

## That's It!
Conversations are now automatically saved to `data/conversations/conversations.json`

---

**For details:** Read `FIX_SUMMARY.md`
**For troubleshooting:** Read `TROUBLESHOOTING_GUIDE.md`
**For testing:** Run `python3 test_conversation_saving.py`
