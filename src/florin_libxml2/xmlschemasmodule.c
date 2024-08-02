#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>
#include <string.h>
#include <libxml/parser.h>
#include <libxml/xmlschemas.h>

#define MSG_MAXSIZE (400)


static PyObject* xmlReadError;


const char* defaultEncoding = "UTF-8";
const int defaultOptions = 0;


void libxml2_destroyXmlDoc(PyObject* capsule)
{
    xmlDocPtr doc = PyCapsule_GetPointer(capsule, "xmlDocPtr");

    xmlFreeDoc(doc);
}


PyObject*
libxml2_xmlschemas_load_schema(PyObject* self, PyObject* args)
{
    char* str = NULL;
    PyObject* capsule = NULL;
    char msg[MSG_MAXSIZE];

    /* Parse arguments */
    if (!PyArg_ParseTuple(args, "s", &str)) {
        return NULL;
    }

    FILE *g = NULL;
    g = fopen("libxml2_error.log", "w");
    xmlDocPtr xmlDoc = NULL;
    xmlInitParser();
    xmlSetGenericErrorFunc(g, fprintf);
    xmlDoc = xmlReadFile(str, defaultEncoding, defaultOptions);
    fclose(g);
    if (xmlDoc == NULL) {
        snprintf(msg, MSG_MAXSIZE, "Could not read the given XML document at given path: '%s'", str);
        PyErr_SetString(PyExc_MemoryError, msg);
        return NULL;
    }
    
    capsule = PyCapsule_New(xmlDoc, "xmlDocPtr", libxml2_destroyXmlDoc);

    return capsule;
}


static PyMethodDef xmlschemasMethods[] = {
    {"load_schema", libxml2_xmlschemas_load_schema, METH_VARARGS, "Load the schema from the given filepath"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef xmlschemasModule = {
    PyModuleDef_HEAD_INIT,
    "xmlschemas",
    "Python interface for the libxml2 xmlschemas module",
    -1,
    xmlschemasMethods
};


PyMODINIT_FUNC
PyInit_xmlschemas(void)
{
    return PyModule_Create(&xmlschemasModule);
}
