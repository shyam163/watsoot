# WhatsApp Bot Troubleshooting Guide

## Issue: Messages Received but Replies Not Sent

This guide helps diagnose and fix the common issue where your WhatsApp bot receives messages but fails to send replies back to users.

## Quick Diagnosis Steps

### 1. Check Environment Configuration

First, verify your `.env` file has real values (not placeholders):

```bash
# Run the diagnostic script
python debug_whatsapp.py
```

**Required Variables:**
- `WHATSAPP_TOKEN` - Your WhatsApp Business API access token
- `WHATSAPP_PHONE_NUMBER_ID` - Your WhatsApp Business phone number ID
- `VERIFY_TOKEN` - Your webhook verification token
- `OPENAI_API_KEY` - Your OpenAI API key
- `OPENAI_ASSISTANT_ID` - Your OpenAI Assistant ID

### 2. Test Your Bot Application

```bash
# Start your bot
python app.py

# In another terminal, test the webhook
python test_webhook.py
```

### 3. Check Server Logs

Look for these log messages when a message is received:

```
📨 Received webhook data: {...}
📱 Incoming message from [phone]: [message]
🔄 Processing message from [phone]: [message]
🤖 Assistant response: [response]...
📤 Sending message to [phone]: [message]...
📊 WhatsApp API Response Status: 200
✅ Message sent successfully: {...}
```

## Common Issues and Solutions

### Issue 1: Configuration Problems

**Symptoms:**
- `❌ WHATSAPP_TOKEN: Missing or using placeholder value`
- `❌ WHATSAPP_PHONE_NUMBER_ID: Missing or using placeholder value`

**Solution:**
1. Get your actual WhatsApp Business API credentials from Meta Developer Console
2. Update your `.env` file with real values
3. Restart your application

### Issue 2: WhatsApp API Authentication Errors

**Symptoms:**
- `❌ WhatsApp API Error: 401`
- `❌ Error Response: {"error":{"message":"Invalid OAuth access token"}}`

**Solution:**
1. Verify your `WHATSAPP_TOKEN` is correct and not expired
2. Check token permissions in Meta Developer Console
3. Generate a new token if needed

### Issue 3: Invalid Phone Number Format

**Symptoms:**
- `❌ WhatsApp API Error: 400`
- Error about invalid phone number format

**Solution:**
1. Ensure phone numbers are in international format (no + sign)
2. Example: Use `1234567890` not `+1-234-567-890`

### Issue 4: OpenAI API Issues

**Symptoms:**
- `❌ Error getting assistant response`
- Messages received but no response generated

**Solution:**
1. Verify `OPENAI_API_KEY` is valid
2. Check `OPENAI_ASSISTANT_ID` exists and is accessible
3. Ensure OpenAI account has sufficient credits

### Issue 5: Webhook Not Receiving Messages

**Symptoms:**
- No `📨 Received webhook data` logs
- Messages sent to bot but no response

**Solution:**
1. Verify webhook URL is publicly accessible
2. Check webhook verification token matches
3. Ensure webhook is properly configured in Meta Developer Console

### Issue 6: Network/Firewall Issues

**Symptoms:**
- `❌ Network error sending WhatsApp message`
- Timeouts or connection errors

**Solution:**
1. Check server internet connectivity
2. Verify firewall allows outbound HTTPS connections
3. Test API connectivity: `curl -I https://graph.facebook.com`

## Debugging Commands

### Test WhatsApp API Directly
```bash
python debug_whatsapp.py
```

### Test Webhook Locally
```bash
python test_webhook.py
```

### Check Application Health
```bash
curl http://your-server:5000/health
```

### View Chat History
```bash
curl http://your-server:5000/active-chats
curl http://your-server:5000/chat-history/PHONE_NUMBER
```

## Log Analysis

### Successful Message Flow
```
📨 Received webhook data: {...}
📱 Incoming message from 1234567890: Hello
🔄 Processing message from 1234567890: Hello
🤖 Assistant response: Hi there! How can I help you?...
📤 Sending message to 1234567890: Hi there! How can I help you?...
📊 WhatsApp API Response Status: 200
✅ Message sent successfully: {"messages":[{"id":"wamid.xxx"}]}
✅ Successfully sent response to 1234567890
```

### Failed Message Flow
```
📨 Received webhook data: {...}
📱 Incoming message from 1234567890: Hello
🔄 Processing message from 1234567890: Hello
🤖 Assistant response: Hi there! How can I help you?...
📤 Sending message to 1234567890: Hi there! How can I help you?...
📊 WhatsApp API Response Status: 400
❌ WhatsApp API Error: 400
❌ Error Response: {"error":{"message":"Invalid parameter"}}
❌ Failed to send response to 1234567890
```

## Meta Developer Console Checklist

1. **App Setup:**
   - WhatsApp Business API product added
   - App is in "Live" mode (not Development)
   - Webhook URL configured and verified

2. **Phone Number:**
   - Phone number added to your WhatsApp Business account
   - Phone number verified and active
   - Correct Phone Number ID copied to `.env`

3. **Webhook Configuration:**
   - Webhook URL: `https://your-domain.com/webhook`
   - Verify Token: Matches your `VERIFY_TOKEN`
   - Webhook fields: `messages` subscribed

4. **Access Token:**
   - System User access token (recommended for production)
   - Token has `whatsapp_business_messaging` permission
   - Token is not expired

## Still Having Issues?

1. **Enable Debug Mode:**
   ```bash
   # In .env file
   FLASK_DEBUG=True
   ```

2. **Check Server Resources:**
   - Ensure server has enough memory/CPU
   - Check disk space for chat logs
   - Monitor network bandwidth

3. **Test with Different Numbers:**
   - Try sending from different WhatsApp numbers
   - Test with numbers in different countries

4. **Contact Support:**
   - Meta Developer Support for API issues
   - OpenAI Support for Assistant issues
   - Your hosting provider for server issues

## Prevention Tips

1. **Monitor Logs Regularly:**
   - Set up log rotation
   - Monitor error rates
   - Alert on API failures

2. **Health Checks:**
   - Implement monitoring for `/health` endpoint
   - Check API token expiration dates
   - Monitor OpenAI usage and credits

3. **Backup Configuration:**
   - Keep backup of working `.env` file
   - Document your Meta Developer Console settings
   - Save working webhook configurations