# -*- coding: utf-8 -*-
"""Write the compact official Sonar category icon used by Touch Portal."""
import base64
import sys


# SteelSeries GG ships this mark as a 40x40 transparent PNG. Touch Portal lays
# out category rows using the complete PNG canvas, including transparent pixels,
# so the output must remain 40x40 rather than placing it on a larger canvas.
SONAR_ICON_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAQkSURBVHgBzVjdUdtAEN49G/wTZ+JUgF/yQyYzsSqIU0FIBZgKIBUAHZAKMBXEqQCnApmZTAK8oFRgMmMMD/g2eydjr06ywbLM8D1gae8kfdzufbt7AE8cCCnh/+rXIQ8NxNwHIGqAoioQVsO30iVfB0AQEOifcAsd732lCykwF0Hf71VVeXWbADf4tg7zISCNn7z1UjDPQ/mHTjw5u9olhB26W6UUmJecwb0E/T+9GqrCdzIrRgkT2J1E8JevpAutuxHh452BtN6HFJhJ8OTsepNQHzCxaoyUxiMm0YabUtfz8HLaO/w/1xyfugmQ60AK4ExyQC3XzrZ9GJQPZpHKEokE/d9XG5jD7445VZAvCuUabMzl4VDaWCqOaFDyHpucQSwGeUMcR2JOQdt7VWkmPWxkB0orTQT1mXWwbjZG/U05tbbeS9A/7e/wT02YAuqXtiCBmNVDlp2xOFOmvOIErWtRbctBG3POZhjJzjGZf4Rg6RAruNIAsXoEw31v/XkACeQgusp3WvgDNASwLIKo1O7EzLlU51tyonFrjJwhNqSv3nqlBUuCJeif902WqE0+rNrujlXlIudgqglTQEO1dNkJZUZDQxppeHsk741rmdweSHKPpIkjHcSGNHLsdaLTViLjJq8mkeO0VrPSkyEsQVS4Nv44cf3mgGu+TXEbuDFnVrh7OjhGRRdYLvTMtbFBVgQhElsJOVbpce1HRCfuMGLxkJNmY2LgQjZXOITMCIoaj7WwF5sla0CKlFXgX7BLkSvq2DPQMC6HBWF38X3paeb4TbHKaW7K2I0j8ld7HE67097L4y0e35TjChaE3SyIHdduYtnzXkbDBWWbQPFQQll3huMLE7SvGsIWZ5KfE3J8Tblm7PuIHyZzEmIZ1AtxG5g/D+5JZmEkOQ3f586ueFNNlqB+E2QWImjFXiRiedRGZENwTDQsLC7j5EwOl6nUINoC2NZAVh+a7HgmLp6FpAKD4/NbfJWHzcitho75WSpB41bMrfrg1Jhw/WwvOs+ucDQZjBr9TF0cfsxIiVoD1BtWP6MKFCTVmCpX2CYxT7aomRMMdY6SKuzEAsMWIgQ7cp6Mz6XHoK0ZuVVNarpEjTmGG5+Zr+CYlEbWOd2GwbPWtB4ay6smX9eEKfDeVg7knMwJPqSrsytnydlDqBC2Olef3LnLWcEZ8M97daSCORSoSTvdwpb3Li7wj0Zw3KoS7rljfP7D5CrtpOdSNbOhbq3ushwcxavvKCko5k1Dv4F5rlLco7twA331Xk9vulISZAFWalKQklX9S64GxGbgkwbkQnj6eWKXN9KX+/qaVAS7Z4MLcHvjh8LucNp3d+s0zB2DC/QaXXbnD7ia7+gu/SG66aVNu4q2I+RjE1iTh+ik4R+/vcPK2+V00OE4S3WI/uTxH70S6oa6nONqAAAAAElFTkSuQmCC"
)


def main(out):
    with open(out, "wb") as icon_file:
        icon_file.write(SONAR_ICON_PNG)
    print("Sonar 40x40 category icon written:", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "icon.png")
