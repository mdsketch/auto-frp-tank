TEMPLATE = """
<html>

<head>
  <style>
    body {
      font-family: sans-serif;
    }

    h1 {
      font-size: 24px;
      font-weight: bold;
      margin-bottom: 10px;
      text-decoration: underline;
    }

    table {
      border-collapse: collapse;
      margin-bottom: 20px;
      width: 100%;
    }

    th,
    td {
      border: 1px solid black;
      padding: 5px;
    }

    th {
      background-color: #ddd;
      text-align: left;
    }

    .category {
      font-weight: bold;
      margin-top: 20px;
      text-decoration: underline;
    }
  </style>
</head>

<body>
  <h1>Tank Design Report</h1>
  <table>
    <tr>
      <th>Thickness</th>
      <td>{{ thickness }} cm</td>
    </tr>
  </table>
  <div class="category">Dimensions</div>
  <table>
    <tr>
      <th>Parameter</th>
      <th>Value</th>
    </tr>
    <tr>
      <td>Diameter</td>
      <td>{{ diameter }} cm</td>
    </tr>
    <tr>
      <td>Height</td>
      <td>{{ height }} cm</td>
    </tr>
    <tr>
      <td>Storage Type</td>
      <td>{{ storage_type }}</td>
    </tr>
    {% if storage_type == 'Liquid' %}
    <tr>
      <td>Specific Gravity</td>
      <td>{{ specific_gravity }}</td>
    </tr>
    {% endif %}
    <tr>
      <td>Internal Pressure</td>
      <td>{{ internal_pressure }} psi</td>
    </tr>
    <tr>
      <td>External Pressure</td>
      <td>{{ external_pressure }} psi</td>
    </tr>
  </table>

  <div class="category">Environment</div>
  <table>
    <tr>
      <th>Parameter</th>
      <th>Value</th>
    </tr>
    {% if outdoor %}
    <tr>
      <td>Compressive Operating Force</td>
      <td>{{ compressive_force }} psi</td>
    </tr>
    <tr>
      <td>Snow Pressure</td>
      <td>{% if snow %}{{ snow_pressure }} psi{% else %}N/A{% endif %}</td>
    </tr>
    <tr>
      <td>Wind Speed</td>
      <td>{% if wind %}{{ wind_speed }} mph{% else %}N/A{% endif %}</td>
    </tr>
    <tr>
      <td>Seismic</td>
      <td>{% if seismic %}{{ seismic_type }}{% else %}N/A{% endif %}</td>
    </tr>
    {% endif %}
    {% if tensile_force %}
    <tr>
      <td>Tensile Operating Force</td>
      <td>{% if tensile_force %}{{ tensile_force_value }} psi{% else %}N/A{% endif %}</td>
    </tr>
    {% endif %}
    {% if tensile_force or outdoor %}
    <tr>
      <td>Operating Moment</td>
      <td>{{ operating_moment }} lb-ft</td>
    </tr>
    {% endif %}

  </table>
  <div class="category">Tank Type</div>
  <table>
    <tr>
      <th>Parameter</th>
      <th>Value</th>
    </tr>
    <tr>
      <td>Tank Type:</td>
      <td>{{ tank_type }}</td>
    </tr>
    <tr>
      <td>Storage Type:</td>
      <td>{{ storage_type }}</td>
    </tr>
    {% if storage_type == 'Liquid' %}
    <tr>
      <td>Specific Gravity:</td>
      <td>{{ specific_gravity }}</td>
    </tr>
    {% endif %}
    {% if corrosion %}
    <tr>
      <td>Corrosion Barrier Thickness (cm):</td>
      <td>{{ corrosion_barrier_thickness }}</td>
    </tr>
    {% if tank_type == 'Dual Laminate' %}
    <tr>
      <td>Corrosion Liner Thickness (cm):</td>
      <td>{{ corrosion_liner_thickness }}</td>
    </tr>
    {% endif %}
    {% endif %}
  </table>
  <div class="category">Top Head</div>
  <table>
    <tr>
      <th>Parameter</th>
      <th>Value</th>
    </tr>
    <tr>
      <td>Type:</td>
      <td>{{ top_head }}</td>
    </tr>
    <tr>
      <td>Live load (kN/m2):</td>
      <td>{{ live_load }}</td>
    </tr>
    <tr>
      <td>Dead load (kN/m2):</td>
      <td>{{ dead_load }}</td>
    </tr>
  </table>

</body>

</html>
"""