'use client'

import { useEffect, useState } from 'react'
import Image from 'next/image'
import { Tab, TabGroup, TabList, TabPanel, TabPanels } from '@headlessui/react'
import clsx from 'clsx'

import { Container } from '@/components/Container'
import backgroundImage from '@/images/background-features.jpg'
import screenshotExpenses from '@/images/screenshots/expenses.png'
import screenshotPayroll from '@/images/screenshots/payroll.png'
import screenshotReporting from '@/images/screenshots/reporting.png'
import screenshotVatReturns from '@/images/screenshots/vat-returns.png'

let global_features = [
  {
    title: 'Patient 1',
    data: [
      {
        "timestamp": "2021-10-01T00:00:00Z",
        "action": "Lights",
        "value": "100%"
      },
      {
        "timestamp": "2021-10-01T00:00:00Z",
        "action": "Nurse Call",
        "value": "Minor"
      },
      {
        "timestamp": "2021-10-01T00:00:00Z",
        "action": "Nurse Call",
        "value": "Major"
      }, 
      {
        "timestamp": "2021-10-01T00:00:00Z",
        "action": "Medicine Dispense",
        "value": "1"
      },
      {
        "timestamp": "2021-10-01T00:00:00Z",
        "action": "Medicine Dispense",
        "value": "2"
      }
    ]
  },
  {
    title: 'Patient 2',
    data: [
      {
        "timestamp": "2021-10-01T00:00:00Z",
        "action": "Lights",
        "value": "100%"
      },
      {
        "timestamp": "2021-10-01T00:00:00Z",
        "action": "Nurse Call",
        "value": "Minor"
      },
      {
        "timestamp": "2021-10-01T00:00:00Z",
        "action": "Nurse Call",
        "value": "Major"
      },
      {
        "timestamp": "2021-10-01T00:00:00Z",
        "action": "Medicine Dispense",
        "value": "1"
      },
      {
        "timestamp": "2021-10-01T00:00:00Z",
        "action": "Medicine Dispense",
        "value": "2"
      }
    ]
  },
  {
    title: 'Patient 3',
    data: [
      {
        "timestamp": "2021-10-01T00:00:00Z",
        "action": "Lights",
        "value": "20%",
      },
      {
        "timestamp": "2021-10-01T00:00:00Z",
        "action": "Nurse Call",
        "value": "Major"
      },
      {
        "timestamp": "2021-10-01T00:00:00Z",
        "action": "Medicine Dispense",
        "value": "1"
      }, 
      {
        "timestamp": "2021-10-01T00:00:00Z",
        "action": "Medicine Dispense",
        "value": "2"
      },
      {
        "timestamp": "2021-10-01T00:00:00Z",
        "action": "Medicine Dispense",
        "value": "3"
      }
    ]
  },
]

export function PrimaryFeatures() {
  let [features, setFeatures] = useState([])
  let [tabOrientation, setTabOrientation] = useState('horizontal')

  async function getData() {
    console.log("hi")
    const response = await fetch('/api')
    console.log(global_features)
    const data = await response.json()
    console.log(data)
    let newFeatures = [{ title: "Patient 1", data: data }].concat(global_features.slice(1, global_features.length))
    console.log(newFeatures)
    setFeatures(newFeatures)
  }

  useEffect(() => {
    setFeatures(features)
    getData()

    let lgMediaQuery = window.matchMedia('(min-width: 1024px)')

    function onMediaQueryChange({ matches }) {
      setTabOrientation(matches ? 'vertical' : 'horizontal')
    }

    onMediaQueryChange(lgMediaQuery)
    lgMediaQuery.addEventListener('change', onMediaQueryChange)

    return () => {
      lgMediaQuery.removeEventListener('change', onMediaQueryChange)
    }
  }, [])

  return (
    <section
      id="dashboard"
      aria-label="Features for running your books"
      className="relative overflow-hidden bg-green-600 pt-20 pb-28 sm:py-32"
    >
      {/* <Image
        className="absolute top-1/2 left-1/2 max-w-none translate-x-[-44%] translate-y-[-42%]"
        src={backgroundImage}
        alt=""
        width={2245}
        height={1636}
        unoptimized
      /> */}
      <Container className="relative">
        <div className="max-w-2xl md:mx-auto md:text-center xl:max-w-none">
          <h2 className="font-display text-3xl tracking-tight text-white sm:text-4xl md:text-5xl">
            Patient Dashboard Demo
          </h2>
          <p className="mt-6 text-lg tracking-tight text-green-100">
            Patient 1 can be updated live by our hardware!
          </p>
        </div>
        <TabGroup
          className="mt-16 grid grid-cols-1 items-center gap-y-2 pt-10 sm:gap-y-6 md:mt-20 lg:grid-cols-12 lg:pt-0"
          vertical={tabOrientation === 'vertical'}
        >
          {({ selectedIndex }) => (
            <>
              <div className="-mx-4 flex overflow-x-auto pb-4 sm:mx-0 sm:overflow-visible sm:pb-0 lg:col-span-2">
                <TabList className="relative z-10 flex gap-x-4 px-4 whitespace-nowrap sm:mx-auto sm:px-0 lg:mx-0 lg:block lg:gap-x-0 lg:gap-y-1 lg:whitespace-normal">
                  {features.map((feature, featureIndex) => (
                    <div
                      key={feature.title}
                      className={clsx(
                        'group relative rounded-full px-4 py-1 lg:rounded-l-xl lg:rounded-r-none lg:p-6',
                        selectedIndex === featureIndex
                          ? 'bg-white lg:bg-white/10 lg:ring-1 lg:ring-white/10 lg:ring-inset'
                          : 'hover:bg-white/10 lg:hover:bg-white/5',
                      )}
                    >
                      <h3>
                        <Tab
                          className={clsx(
                            'font-display text-lg data-selected:not-data-focus:outline-hidden',
                            selectedIndex === featureIndex
                              ? 'text-green-600 lg:text-white'
                              : 'text-green-100 hover:text-white lg:text-white',
                          )}
                        >
                          <span className="absolute inset-0 rounded-full lg:rounded-l-xl lg:rounded-r-none" />
                          {feature.title}
                        </Tab>
                      </h3>
                      {/* <p
                        className={clsx(
                          'mt-2 hidden text-sm lg:block',
                          selectedIndex === featureIndex
                            ? 'text-white'
                            : 'text-green-100 group-hover:text-white',
                        )}
                      >
                        {feature.description}
                      </p> */}
                    </div>
                  ))}
                </TabList>
              </div>
              <TabPanels className="lg:col-span-10">
                {features.map((feature) => (
                  <TabPanel key={feature.title} unmount={false}>
                    <div className="relative sm:px-6 lg:hidden">
                      <div className="absolute -inset-x-4 top-[-6.5rem] bottom-[-4.25rem] bg-white/10 ring-1 ring-white/10 ring-inset sm:inset-x-0 sm:rounded-t-xl" />
                      <p className="relative mx-auto max-w-2xl text-base text-white sm:text-center">
                        {feature.description}
                      </p>
                    </div>
                    <div className="mt-10 w-[45rem] overflow-hidden rounded-xl bg-slate-50 shadow-xl shadow-green-900/20 sm:w-auto lg:mt-0 lg:w-[67.8125rem]">


                      <div className="relative overflow-x-auto shadow-md sm:rounded-lg">
                        <table className="w-full text-sm text-left rtl:text-right text-gray-500">
                          <thead className="text-xs text-gray-700 uppercase bg-gray-200">
                            <tr>
                              <th scope="col" className="px-6 py-3">
                                Timestamp
                              </th>
                              <th scope="col" className="px-6 py-3">
                                Action
                              </th>
                              <th scope="col" className="px-6 py-3">
                                Value
                              </th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr className="bg-gray-100 border-b border-gray-200 hover:bg-gray-200">
                              <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap">
                                {feature.data[0].timestamp}
                              </th>
                              <td className="px-6 py-4">
                                {feature.data[0].action}
                              </td>
                              <td className="px-6 py-4">
                                {feature.data[0].value}
                              </td>
                            </tr>
                            <tr className="bg-gray-100 border-b border-gray-200 hover:bg-gray-200">
                              <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap">
                                {feature.data[1].timestamp}
                              </th>
                              <td className="px-6 py-4">
                                {feature.data[1].action}
                              </td>
                              <td className="px-6 py-4">
                                {feature.data[1].value}
                              </td>
                            </tr>
                            <tr className="bg-gray-100 hover:bg-gray-200">
                              <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap">
                                {feature.data[2].timestamp}
                              </th>
                              <td className="px-6 py-4">
                                {feature.data[2].action}
                              </td>
                              <td className="px-6 py-4">
                                {feature.data[2].value}
                              </td>
                            </tr>
                            <tr className="bg-gray-100 hover:bg-gray-200">
                              <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap">
                                {feature.data[3].timestamp}
                              </th>
                              <td className="px-6 py-4">
                                {feature.data[3].action}
                              </td>
                              <td className="px-6 py-4">
                                {feature.data[3].value}
                              </td>
                            </tr>
                            <tr className="bg-gray-100 hover:bg-gray-200">
                              <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap">
                                {feature.data[4].timestamp}
                              </th>
                              <td className="px-6 py-4">
                                {feature.data[4].action}
                              </td>
                              <td className="px-6 py-4">
                                {feature.data[4].value}
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>

                    </div>
                  </TabPanel>
                ))}
              </TabPanels>
            </>
          )}
        </TabGroup>
      </Container>
    </section>
  )
}
