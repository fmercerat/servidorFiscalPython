using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ServidorPythonEpson
{
    public class CierreZ
    {
        public int Funcion { get; set; }

        public CierreZ()
        {
            Funcion = 1;
        }

        public string ObtenerJSON()
        {
            return JsonConvert.SerializeObject(this);
        }
    }
}
