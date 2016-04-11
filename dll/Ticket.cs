using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace ServidorPythonEpson
{
    public class Ticket
    {
        public decimal Descuentos { get; set; }
        public decimal Devoluciones { get; set; }
        public decimal InteresTarjeta { get; set; }
        public List<Item> Items { get; set; }
        public int Funcion { get; set; }

        public Ticket()
        {
            Descuentos = 0;
            Devoluciones = 0;
            InteresTarjeta = 0;
            Items = new List<Item>();
            Funcion = 0;
        }

        public void AgregarItem(Item i)
        {
            Items.Add(i);
        }

        public string ObtenerJson()
        {
            return JsonConvert.SerializeObject(this);
        }
    }
}
