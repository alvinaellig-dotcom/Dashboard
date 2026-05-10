const css = getComputedStyle(document.documentElement);
const colors = {
  teal: css.getPropertyValue("--teal").trim(),
  gold: css.getPropertyValue("--gold").trim(),
  green: css.getPropertyValue("--green").trim(),
  red: css.getPropertyValue("--red").trim(),
  blue: css.getPropertyValue("--blue").trim(),
  text: css.getPropertyValue("--text").trim(),
  muted: css.getPropertyValue("--muted").trim(),
  border: "rgba(148, 163, 184, 0.16)",
};

Chart.defaults.color = colors.muted;
Chart.defaults.borderColor = colors.border;
Chart.defaults.font.family =
  'Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif';

const sharedOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    intersect: false,
    mode: "index",
  },
  plugins: {
    legend: {
      labels: {
        boxWidth: 10,
        boxHeight: 10,
        usePointStyle: true,
      },
    },
    tooltip: {
      backgroundColor: "rgba(5, 10, 19, 0.92)",
      borderColor: colors.border,
      borderWidth: 1,
      padding: 10,
      titleColor: colors.text,
    },
  },
  scales: {
    x: {
      grid: {
        display: false,
      },
    },
    y: {
      grid: {
        color: "rgba(148, 163, 184, 0.1)",
      },
    },
  },
};

function makeGradient(ctx, color) {
  const gradient = ctx.createLinearGradient(0, 0, 0, 220);
  gradient.addColorStop(0, `${color}55`);
  gradient.addColorStop(1, `${color}05`);
  return gradient;
}

function chart(id, config) {
  const canvas = document.getElementById(id);
  return new Chart(canvas, config);
}

const labels12 = ["Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez", "Jan", "Feb", "Mrz", "Apr", "Mai"];

chart("fearGreedChart", {
  type: "doughnut",
  data: {
    labels: ["Greed", "Rest"],
    datasets: [
      {
        data: [69, 31],
        backgroundColor: [colors.gold, "rgba(148, 163, 184, 0.14)"],
        borderWidth: 0,
        circumference: 220,
        rotation: 250,
        cutout: "74%",
      },
    ],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: { enabled: false },
    },
  },
});

const chfUsdCanvas = document.getElementById("chfUsdChart").getContext("2d");
chart("chfUsdChart", {
  type: "line",
  data: {
    labels: ["29. Apr", "30. Apr", "1. Mai", "4. Mai", "5. Mai", "6. Mai", "7. Mai"],
    datasets: [
      {
        label: "CHF/USD",
        data: [0.7762, 0.7774, 0.7791, 0.7786, 0.7803, 0.7804, 0.781816],
        borderColor: colors.teal,
        backgroundColor: makeGradient(chfUsdCanvas, colors.teal),
        borderWidth: 2.5,
        fill: true,
        tension: 0.38,
      },
    ],
  },
  options: {
    ...sharedOptions,
    plugins: {
      ...sharedOptions.plugins,
      legend: { display: false },
    },
    scales: {
      ...sharedOptions.scales,
      y: {
        ...sharedOptions.scales.y,
        min: 0.774,
        ticks: {
          callback: (value) => Number(value).toFixed(3),
        },
      },
    },
  },
});

const repoData = [
  { label: "GCF Repo Rate", value: "4.42%", change: "+3 bp", tone: "positive" },
  { label: "Tri-Party Repo Rate", value: "4.36%", change: "+1 bp", tone: "positive" },
  { label: "Volumen", value: "$2.41T", change: "-1.8%", tone: "negative" },
  { label: "Tagesveraenderung", value: "+$18B", change: "Liquiditaet", tone: "positive" },
];

document.getElementById("repoStats").innerHTML = repoData
  .map(
    (item) => `
      <div class="repo-stat">
        ${item.label}
        <strong>${item.value}</strong>
        <span class="${item.tone}">${item.change}</span>
      </div>
    `,
  )
  .join("");

chart("repoChart", {
  type: "bar",
  data: {
    labels: ["Mo", "Di", "Mi", "Do", "Fr"],
    datasets: [
      {
        label: "GCF Repo Rate",
        data: [4.36, 4.38, 4.39, 4.39, 4.42],
        backgroundColor: colors.blue,
        borderRadius: 8,
      },
      {
        label: "Tri-Party Repo Rate",
        data: [4.31, 4.33, 4.34, 4.35, 4.36],
        backgroundColor: colors.teal,
        borderRadius: 8,
      },
    ],
  },
  options: {
    ...sharedOptions,
    scales: {
      ...sharedOptions.scales,
      y: {
        ...sharedOptions.scales.y,
        ticks: {
          callback: (value) => `${value}%`,
        },
      },
    },
  },
});

chart("fedChart", {
  type: "line",
  data: {
    labels: labels12,
    datasets: [
      {
        label: "Fed-Bilanz, M USD",
        data: [6915000, 6888500, 6849400, 6822300, 6790100, 6765500, 6741800, 6729200, 6719800, 6730100, 6732405, 6709505],
        borderColor: colors.blue,
        backgroundColor: "rgba(56, 189, 248, 0.12)",
        borderWidth: 2.5,
        fill: true,
        pointRadius: 0,
        tension: 0.35,
      },
    ],
  },
  options: {
    ...sharedOptions,
    plugins: {
      ...sharedOptions.plugins,
      legend: { display: false },
    },
    scales: {
      ...sharedOptions.scales,
      y: {
        ...sharedOptions.scales.y,
        ticks: {
          callback: (value) => `${Math.round(value / 1000)}k`,
        },
      },
    },
  },
});

chart("privateDebtChart", {
  type: "line",
  data: {
    labels: ["2020", "2021", "2022", "2023", "2024", "2025", "2026"],
    datasets: [
      {
        label: "Privatkreditschulden Index",
        data: [100, 108, 116, 129, 139, 148, 154],
        borderColor: colors.gold,
        backgroundColor: "rgba(245, 197, 66, 0.12)",
        borderWidth: 2.5,
        fill: true,
        tension: 0.34,
      },
      {
        label: "Trend",
        data: [101, 109, 118, 127, 136, 146, 156],
        borderColor: colors.green,
        borderDash: [6, 6],
        pointRadius: 0,
        borderWidth: 2,
      },
    ],
  },
  options: sharedOptions,
});

chart("uraniumSpotChart", {
  type: "line",
  data: {
    labels: ["Nov", "Dez", "Jan", "Feb", "Mrz", "Apr"],
    datasets: [
      {
        label: "USD/lb",
        data: [75.4, 78.2, 80.5, 82.1, 82.85, 86.35],
        borderColor: colors.gold,
        borderWidth: 2.5,
        pointRadius: 0,
        tension: 0.4,
      },
    ],
  },
  options: {
    ...sharedOptions,
    plugins: { ...sharedOptions.plugins, legend: { display: false } },
  },
});

chart("nuclearShareChart", {
  type: "line",
  data: {
    labels: ["2020", "2022", "2024", "2026", "2030"],
    datasets: [
      {
        label: "Anteil am Strommix",
        data: [9.8, 9.9, 10.1, 10.5, 11.7],
        borderColor: colors.green,
        backgroundColor: "rgba(34, 197, 94, 0.12)",
        borderWidth: 2.5,
        fill: true,
        tension: 0.38,
      },
    ],
  },
  options: {
    ...sharedOptions,
    plugins: { ...sharedOptions.plugins, legend: { display: false } },
    scales: {
      ...sharedOptions.scales,
      y: {
        ...sharedOptions.scales.y,
        ticks: {
          callback: (value) => `${value}%`,
        },
      },
    },
  },
});

chart("uraniumForecastChart", {
  type: "bar",
  data: {
    labels: ["2026", "2030", "2040"],
    datasets: [
      {
        label: "Uranenergie Index",
        data: [100, 122, 168],
        backgroundColor: [colors.teal, colors.blue, colors.green],
        borderRadius: 10,
      },
    ],
  },
  options: {
    ...sharedOptions,
    plugins: { ...sharedOptions.plugins, legend: { display: false } },
  },
});

chart("powerMixChart", {
  type: "line",
  data: {
    labels: ["2020", "2022", "2024", "2026", "2030", "2040"],
    datasets: [
      {
        label: "Solar",
        data: [3.2, 4.7, 6.5, 8.9, 14.5, 25.0],
        borderColor: colors.gold,
        backgroundColor: "rgba(245, 197, 66, 0.08)",
        fill: true,
        tension: 0.35,
      },
      {
        label: "Wind",
        data: [6.0, 7.5, 9.1, 11.4, 15.8, 22.0],
        borderColor: colors.teal,
        backgroundColor: "rgba(45, 212, 191, 0.08)",
        fill: true,
        tension: 0.35,
      },
      {
        label: "Nuclear",
        data: [9.8, 9.9, 10.1, 10.5, 11.7, 14.0],
        borderColor: colors.green,
        backgroundColor: "rgba(34, 197, 94, 0.08)",
        fill: true,
        tension: 0.35,
      },
      {
        label: "Fossil",
        data: [61, 59, 57, 54, 47, 34],
        borderColor: colors.red,
        borderDash: [6, 6],
        tension: 0.35,
      },
    ],
  },
  options: {
    ...sharedOptions,
    scales: {
      ...sharedOptions.scales,
      y: {
        ...sharedOptions.scales.y,
        ticks: {
          callback: (value) => `${value}%`,
        },
      },
    },
  },
});

const shortages = [
  ["Kupfer", "Grid, EV, Rechenzentren", "high"],
  ["Lithium", "Batterien, Raffination", "medium"],
  ["Seltene Erden", "Magnete, Defense", "high"],
  ["Stahl", "Netzausbau, Baukosten", "medium"],
  ["Halbleiter", "AI, Automatisierung", "medium"],
  ["Uran", "Minenangebot, Konversion", "high"],
];

document.getElementById("shortageList").innerHTML = shortages
  .map(
    ([name, driver, risk]) => `
      <div class="shortage-item">
        <div>
          <strong>${name}</strong>
          <span>${driver}</span>
        </div>
        <em class="risk risk-${risk}">${risk}</em>
      </div>
    `,
  )
  .join("");

const reserveData = [
  ["USA", 372],
  ["Saudi-Arabien", 296],
  ["China", 220],
  ["Irak", 145],
  ["UAE", 110],
  ["Russland", 98],
];

chart("oilReserveChart", {
  type: "bar",
  data: {
    labels: reserveData.map(([country]) => country),
    datasets: [
      {
        label: "Strategische Oelreserven, Mio. Barrel",
        data: reserveData.map(([, value]) => value),
        backgroundColor: [colors.blue, colors.gold, colors.teal, colors.green, "#60a5fa", colors.red],
        borderRadius: 10,
      },
    ],
  },
  options: {
    ...sharedOptions,
    indexAxis: "y",
    plugins: {
      ...sharedOptions.plugins,
      legend: { display: false },
    },
    scales: {
      ...sharedOptions.scales,
      x: {
        ...sharedOptions.scales.x,
        grid: {
          color: "rgba(148, 163, 184, 0.1)",
        },
        ticks: {
          callback: (value) => `${value}M`,
        },
      },
      y: {
        ...sharedOptions.scales.y,
        grid: {
          display: false,
        },
      },
    },
  },
});

document.getElementById("reserveTable").innerHTML = reserveData
  .map(
    ([country, value]) => `
      <div class="reserve-row">
        <span>${country}</span>
        <strong>${value}M bbl</strong>
      </div>
    `,
  )
  .join("");
