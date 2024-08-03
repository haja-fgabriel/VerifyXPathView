#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>
#include <string.h>
#include <libxml/parser.h>
#include <libxml/xmlschemas.h>

#define MSG_MAXSIZE (400)


static PyObject* xmlReadError;

static PyObject* LibxmlInternalError = NULL;

const char* defaultEncoding = "UTF-8";
const int defaultOptions = 0;


void handleLibxmlError(void *ctx ATTRIBUTE_UNUSED, const char *msg, ...)
{
    va_list args;
    char formatted[MSG_MAXSIZE];
    char displayed[MSG_MAXSIZE + 100];

    va_start(args, msg);
    vsprintf_s(formatted, MSG_MAXSIZE, msg, args);
    va_end(args);

    sprintf_s(displayed, MSG_MAXSIZE + 100, "Internal error occured in the libxml2 library:\n%s", formatted);
    
    PyErr_SetString(LibxmlInternalError, displayed);
}


void libxml2_destroyXmlSchema(PyObject* capsule)
{
    xmlSchemaPtr schema = PyCapsule_GetPointer(capsule, "xmlSchemaPtr");
    xmlSchemaFree(schema);
}


PyObject*
libxml2_xmlschemas_load_schema(PyObject* self, PyObject* args)
{
    char* str = NULL;
    PyObject* capsule = NULL;
    PyObject* capsule2 = NULL;
    PyObject* result = NULL;
    PyObject* dictResult = NULL;

    void* todoCtx = NULL;
    xmlSchemaParserCtxtPtr xmlSchemaParser = NULL;
    xmlSchemaPtr xmlSchema = NULL;

    char msg[MSG_MAXSIZE];

    /* Parse arguments */
    if (!PyArg_ParseTuple(args, "s", &str)) {
        return NULL;
    }

    xmlInitParser();
    xmlSetGenericErrorFunc(todoCtx, handleLibxmlError);

    xmlSchemaParser = xmlSchemaNewParserCtxt(str);
    if (xmlSchemaParser == NULL) {
        return NULL;
    }

    xmlSchema = xmlSchemaParse(xmlSchemaParser);
    xmlSchemaFreeParserCtxt(xmlSchemaParser);
    if (xmlSchema == NULL) {
        return NULL;
    }

    xmlSchemaValidCtxtPtr validCtxt = xmlSchemaNewValidCtxt(xmlSchema);
    if (validCtxt == NULL) {
        xmlSchemaFree(xmlSchema);
        return NULL;
    }

    int retVal = xmlSchemaIsValid(validCtxt);
    if (retVal < 0) {
        xmlSchemaFreeValidCtxt(validCtxt);
        xmlSchemaFree(xmlSchema);
        return NULL;
    }

    if (retVal == 0) {
        xmlSchemaFreeValidCtxt(validCtxt);
        xmlSchemaFree(xmlSchema);
        return NULL;
    }

    capsule = PyCapsule_New(xmlSchema, "xmlSchemaPtr", libxml2_destroyXmlSchema);

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
    PyObject* module = PyModule_Create(&xmlschemasModule);

    if (module == NULL) {
        return NULL;
    }

    /* Declare a new Python exception class 
     * Equivalent to 
     * ```python
     * class LibxmlInternalError(Exception):
     *     pass
     * ```
     */
    LibxmlInternalError = PyErr_NewException("xmlschemas.LibxmlInternalError", NULL, NULL);
    if (LibxmlInternalError == NULL) {
        Py_DECREF(module);
        return NULL;
    }

    /* Manually add the exception class to the module. */
    Py_INCREF(LibxmlInternalError);
    if (PyModule_AddObject(module, "LibxmlInternalError", LibxmlInternalError) < 0) {
        Py_DECREF(LibxmlInternalError);
        Py_DECREF(module);
        return NULL;
    }

    return module;
}
