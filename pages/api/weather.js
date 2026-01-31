export default async function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  try {
    const response = await fetch(
      'https://api.open-meteo.com/v1/forecast?latitude=37.0017&longitude=35.3289&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=Europe%2FIstanbul&forecast_days=3'
    )

    if (!response.ok) {
      throw new Error('Hava durumu verisi alınamadı')
    }

    const data = await response.json()
    res.status(200).json(data)
  } catch (error) {
    res.status(500).json({ error: 'Hava durumu bilgisi alınamadı' })
  }
}
