/**
 * Cloudflare Worker for Backup Automation
 * Serverless backup execution compatible with AUDITORIA360
 */

export default {
  async scheduled(event, env) {
    // Handle scheduled backup events
    console.log('Backup automation triggered by Cloudflare Cron');
    
    try {
      const backupResult = await executeBackupRoutine(env);
      console.log('Backup completed:', backupResult);
      return backupResult;
    } catch (error) {
      console.error('Backup failed:', error);
      await notifyBackupFailure(error, env);
      throw error;
    }
  },

  async fetch(request, env) {
    // Handle manual backup triggers via HTTP
    const url = new URL(request.url);
    
    if (url.pathname === '/backup' && request.method === 'POST') {
      try {
        // Verify authorization
        const authHeader = request.headers.get('Authorization');
        if (!authHeader || !isValidAuth(authHeader, env)) {
          return new Response('Unauthorized', { status: 401 });
        }
        
        const backupType = url.searchParams.get('type') || 'full';
        const result = await executeBackupRoutine(env, backupType);
        
        return new Response(JSON.stringify({
          success: true,
          result: result,
          timestamp: new Date().toISOString()
        }), {
          headers: { 'Content-Type': 'application/json' }
        });
        
      } catch (error) {
        return new Response(JSON.stringify({
          success: false,
          error: error.message,
          timestamp: new Date().toISOString()
        }), {
          status: 500,
          headers: { 'Content-Type': 'application/json' }
        });
      }
    }
    
    if (url.pathname === '/backup/status') {
      return new Response(JSON.stringify({
        status: 'operational',
        service: 'AUDITORIA360 Backup Worker',
        version: '1.0.0',
        last_backup: await getLastBackupInfo(env),
        timestamp: new Date().toISOString()
      }), {
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    return new Response('Not Found', { status: 404 });
  }
};

async function executeBackupRoutine(env, backupType = 'full') {
  const apiBaseUrl = env.API_BASE_URL || 'https://auditoria360.vercel.app/api';
  const authToken = env.API_AUTH_TOKEN;
  
  if (!authToken) {
    throw new Error('API_AUTH_TOKEN not configured');
  }
  
  // Call the backup API endpoint
  const backupResponse = await fetch(`${apiBaseUrl}/v1/automation/backup/daily`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${authToken}`,
      'Content-Type': 'application/json',
      'User-Agent': 'AUDITORIA360-CF-Worker/1.0'
    },
    body: JSON.stringify({
      type: backupType,
      source: 'cloudflare_worker',
      scheduled: true
    })
  });
  
  if (!backupResponse.ok) {
    throw new Error(`Backup API call failed: ${backupResponse.status} ${backupResponse.statusText}`);
  }
  
  const result = await backupResponse.json();
  
  // Store backup metadata in Cloudflare KV
  if (env.BACKUP_METADATA) {
    await env.BACKUP_METADATA.put(
      `backup_${new Date().toISOString().split('T')[0]}`, 
      JSON.stringify({
        ...result,
        worker_execution: {
          timestamp: new Date().toISOString(),
          type: backupType,
          cf_ray: env.CF_RAY || 'unknown'
        }
      }),
      { expirationTtl: 60 * 60 * 24 * 31 } // 31 days
    );
  }
  
  return result;
}

async function getLastBackupInfo(env) {
  if (!env.BACKUP_METADATA) {
    return null;
  }
  
  try {
    // Get today's backup info
    const today = new Date().toISOString().split('T')[0];
    const lastBackup = await env.BACKUP_METADATA.get(`backup_${today}`, 'json');
    
    if (lastBackup) {
      return {
        date: today,
        status: lastBackup.status,
        timestamp: lastBackup.worker_execution?.timestamp
      };
    }
    
    // If no backup today, try yesterday
    const yesterday = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString().split('T')[0];
    const yesterdayBackup = await env.BACKUP_METADATA.get(`backup_${yesterday}`, 'json');
    
    if (yesterdayBackup) {
      return {
        date: yesterday,
        status: yesterdayBackup.status,
        timestamp: yesterdayBackup.worker_execution?.timestamp
      };
    }
    
    return null;
  } catch (error) {
    console.error('Error getting last backup info:', error);
    return null;
  }
}

function isValidAuth(authHeader, env) {
  // Simple validation - in production, use proper JWT validation
  const expectedToken = env.WORKER_AUTH_TOKEN || 'backup-worker-secret';
  return authHeader === `Bearer ${expectedToken}`;
}

async function notifyBackupFailure(error, env) {
  if (!env.NOTIFICATION_WEBHOOK) {
    console.log('No notification webhook configured');
    return;
  }
  
  try {
    await fetch(env.NOTIFICATION_WEBHOOK, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        service: 'AUDITORIA360 Backup',
        status: 'failed',
        error: error.message,
        timestamp: new Date().toISOString(),
        source: 'cloudflare_worker'
      })
    });
  } catch (notifyError) {
    console.error('Failed to send notification:', notifyError);
  }
}