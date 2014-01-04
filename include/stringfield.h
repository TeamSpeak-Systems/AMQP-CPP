/**
 *  String field types for amqp
 * 
 *  @copyright 2014 Copernica BV
 */

/**
 *  Set up namespace
 */
namespace AMQP {

/**
 *  Base class for string types
 */
template <typename T, char F>
class StringField : public Field
{
private:
    /**
     *  Pointer to string data
     *  @var string
     */
    std::string _data;

public:
    /**
     *  Initialize empty string
     */
    StringField() {}

    /**
     *  Construct based on a std::string
     *
     *  @param  value   string value
     */
    StringField(std::string value) : _data(value) {}

    /**
     *  Construct based on received data
     *  @param  frame
     */
    StringField(ReceivedFrame &frame)
    {
        // get the size
        T size(frame);
        
        // read data
        const char *data = frame.nextData(size.value());
        
        // @todo what if this fails?
        
        // allocate string
        _data = std::string((char*) data, (size_t) size.value());
    }

    /**
     *  Clean up memory used
     */
    virtual ~StringField() {}

    /**
     *  Create a new instance of this object
     *  @return Field*
     * 
     *  @todo   can this be protected?
     *  @todo   check if all clone methods have a override keyword
     */
    virtual Field *clone() const override
    {
        // create a new copy of ourselves and return it
        return new StringField(_data);
    }

    /**
     *  Assign a new value
     *
     *  @param  value   new value
     */
    StringField& operator=(const std::string& value)
    {
        // overwrite data
        _data = value;

        // allow chaining
        return *this;
    }

    /**
     *  Get the size this field will take when
     *  encoded in the AMQP wire-frame format
     */
    virtual size_t size() const override
    {
        // find out size of the size parameter
        T size(_data.size());
        
        // size of the uint8 or uint32 + the actual string size
        return size.size() + _data.size();
    }

    /**
     *  Get the value
     *  @return string
     */
    operator const std::string& () const
    {
        return _data;
    }

    /**
     *  Get the value
     *  @return string
     */
    const std::string& value() const
    {
        // get data
        return _data;
    }

    /**
     *  Get the maximum allowed string length for this field
     *  @return size_t
     */
    constexpr static size_t maxLength()
    {
        return T::max();
    }

    /**
     *  Write encoded payload to the given buffer.
     *  @param  buffer
     */
    virtual void fill(OutBuffer& buffer) const override
    {
        // create size
        T size(_data.size());
        
        // first, write down the size of the string
        size.fill(buffer);

        // write down the string content
        buffer.add(_data);
    }

    /**
     *  Get the type ID that is used to identify this type of
     *  field in a field table
     *  @return char
     */
    virtual char typeID() const override
    {
        return F;
    }
};

/**
 *  Concrete string types for AMQP
 */
typedef StringField<UOctet, 's'>    ShortString;
typedef StringField<ULong, 'S'>     LongString;

/**
 *  end namespace
 */
}
