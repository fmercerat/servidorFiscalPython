using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ServidorPythonEpson
{
    public class CierreX
    {
        public int Funcion { get; set; }

        public CierreX()
        {
            Funcion = 2;
        }

        public string ObtenerJSON()
        {
            return JsonConvert.SerializeObject(this);
        }
    }
}
