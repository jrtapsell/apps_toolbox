import puppeteer from 'puppeteer';

(async () => {
  const browser = await puppeteer.launch()
  const page = await browser.newPage()
  for (const [resolutionname, settings] of [
    ['pixel_6_pro', {
      width: 412,
      height: 892,
      deviceScaleFactor: 3.5,
      hasTouch: true,
      isMobile: true
    }],
    ['iphone_15', {
      width: 393,
      height: 852,
      deviceScaleFactor: 3,
      hasTouch: true,
      isMobile: true
    }],
    ['laptop', {
      width: 1846,
      height: 932,
      deviceScaleFactor: 1,
      hasTouch: true,
      isLandscape: true,
      isMobile: true
    }]
  ]) {
    await page.setViewport(settings)
    await page.goto('http://localhost:8000')
    for (const currentmode of [
      'none',
      'achromatopsia',
      'blurredVision',
      'deuteranopia',
      'protanopia',
      'tritanopia'
    ]) {
      await page.emulateVisionDeficiency(currentmode)
      await page.screenshot({ path: `screenshots/${resolutionname}_${currentmode}.png` })
      await page.screenshot({ path: `screenshots/${resolutionname}_${currentmode}_full.png`, fullPage: true, captureBeyondViewport: true })
    }
  }

  await browser.close()
})()
