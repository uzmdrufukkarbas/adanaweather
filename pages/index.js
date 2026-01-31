import { useEffect, useState } from 'react'
import Head from 'next/head'

const getWeatherDescription = (code) => {
  const descriptions = {
    0: 'Açık',
    1: 'Çoğunlukla Açık',
    2: 'Parçalı Bulutlu',
    3: 'Bulutlu',
    45: 'Sisli',
    48: 'Dondurucu Sisli',
    51: 'Hafif Çiseleyen',
    53: 'Çiseleyen',
    55: 'Yoğun Çiseleyen',
    61: 'Hafif Yağmurlu',
    63: 'Yağmurlu',
    65: 'Şiddetli Yağmurlu',
    71: 'Hafif Karlı',
    73: 'Karlı',
    75: 'Şiddetli Karlı',
    77: 'Dolu',
    80: 'Sağanak Yağışlı',
    81: 'Orta Sağanak',
    82: 'Şiddetli Sağanak',
    85: 'Hafif Kar Sağanağı',
    86: 'Şiddetli Kar Sağanağı',
    95: 'Gök Gürültülü Fırtına',
    96: 'Dolulu Fırtına',
    99: 'Şiddetli Dolulu Fırtına',
  }
  return descriptions[code] || 'Bilinmiyor'
}

const getWeatherIcon = (code) => {
  if (code === 0) return '☀️'
  if (code <= 3) return '⛅'
  if (code <= 48) return '🌫️'
  if (code <= 55) return '🌦️'
  if (code <= 65) return '🌧️'
  if (code <= 77) return '🌨️'
  if (code <= 82) return '⛈️'
  if (code <= 86) return '❄️'
  return '⚡'
}

export default function Home() {
  const [weather, setWeather] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchWeather = async () => {
      try {
        const response = await fetch('/api/weather')
        if (!response.ok) {
          throw new Error('Hava durumu bilgisi alınamadı')
        }
        const data = await response.json()
        setWeather(data)
        setLoading(false)
      } catch (err) {
        setError('Hava durumu yüklenirken bir hata oluştu')
        setLoading(false)
      }
    }

    fetchWeather()
    const interval = setInterval(fetchWeather, 600000)
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return (
      <>
        <Head>
          <title>Adana Hava Durumu</title>
          <meta name="description" content="Adana için güncel hava durumu bilgileri" />
          <meta name="viewport" content="width=device-width, initial-scale=1" />
        </Head>
        <main className="flex min-h-screen items-center justify-center">
          <div className="text-white text-2xl">Yükleniyor...</div>
        </main>
      </>
    )
  }

  if (error || !weather) {
    return (
      <>
        <Head>
          <title>Adana Hava Durumu</title>
          <meta name="description" content="Adana için güncel hava durumu bilgileri" />
          <meta name="viewport" content="width=device-width, initial-scale=1" />
        </Head>
        <main className="flex min-h-screen items-center justify-center">
          <div className="text-white text-2xl">{error || 'Bir hata oluştu'}</div>
        </main>
      </>
    )
  }

  const today = new Date().toLocaleDateString('tr-TR', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })

  return (
    <>
      <Head>
        <title>Adana Hava Durumu</title>
        <meta name="description" content="Adana için güncel hava durumu bilgileri" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>
      <main className="flex min-h-screen items-center justify-center p-4">
        <div className="w-full max-w-4xl">
          <div className="bg-white/10 backdrop-blur-lg rounded-3xl shadow-2xl p-8 mb-6 text-white">
            <div className="text-center mb-8">
              <h1 className="text-5xl font-bold mb-2">Adana</h1>
              <p className="text-lg opacity-90">{today}</p>
            </div>

            <div className="flex flex-col md:flex-row items-center justify-around gap-8">
              <div className="text-center">
                <div className="text-8xl mb-4">
                  {getWeatherIcon(weather.current.weather_code)}
                </div>
                <p className="text-2xl font-semibold">
                  {getWeatherDescription(weather.current.weather_code)}
                </p>
              </div>

              <div className="text-center">
                <div className="text-7xl font-bold mb-2">
                  {Math.round(weather.current.temperature_2m)}°
                </div>
                <p className="text-xl opacity-90">
                  Hissedilen: {Math.round(weather.current.apparent_temperature)}°
                </p>
              </div>

              <div className="grid grid-cols-2 gap-6 text-center">
                <div className="bg-white/10 rounded-xl p-4">
                  <p className="text-sm opacity-75 mb-1">Nem</p>
                  <p className="text-2xl font-semibold">
                    {weather.current.relative_humidity_2m}%
                  </p>
                </div>
                <div className="bg-white/10 rounded-xl p-4">
                  <p className="text-sm opacity-75 mb-1">Rüzgar</p>
                  <p className="text-2xl font-semibold">
                    {Math.round(weather.current.wind_speed_10m)} km/s
                  </p>
                </div>
                <div className="bg-white/10 rounded-xl p-4 col-span-2">
                  <p className="text-sm opacity-75 mb-1">Yağış</p>
                  <p className="text-2xl font-semibold">
                    {weather.current.precipitation} mm
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {weather.daily.time.slice(0, 3).map((date, index) => {
              const dayDate = new Date(date)
              const dayName = dayDate.toLocaleDateString('tr-TR', {
                weekday: 'short',
              })
              
              return (
                <div
                  key={date}
                  className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 text-white text-center"
                >
                  <h3 className="text-xl font-semibold mb-3">
                    {index === 0 ? 'Bugün' : dayName}
                  </h3>
                  <div className="text-5xl mb-3">
                    {getWeatherIcon(weather.daily.weather_code[index])}
                  </div>
                  <p className="text-lg mb-3">
                    {getWeatherDescription(weather.daily.weather_code[index])}
                  </p>
                  <div className="flex justify-center gap-4 text-lg">
                    <span className="font-semibold">
                      {Math.round(weather.daily.temperature_2m_max[index])}°
                    </span>
                    <span className="opacity-75">
                      {Math.round(weather.daily.temperature_2m_min[index])}°
                    </span>
                  </div>
                </div>
              )
            })}
          </div>

          <div className="text-center mt-6 text-white/60 text-sm">
            Veriler Open-Meteo API&apos;den alınmaktadır
          </div>
        </div>
      </main>
    </>
  )
}
