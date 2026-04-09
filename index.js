const express = require("express");

const app = express();
app.use(express.json());

function setName(name) {
  return name;
}

app.post("/set-name", (req, res) => {
  const { name } = req.body;

  // Code injection via eval string construction
  eval("setName('" + name + "')");

  res.json({ ok: true });
});

app.listen(3000);
